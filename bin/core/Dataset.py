from os import listdir, path
import os
import numpy as np
from collections import defaultdict, OrderedDict
import re
import glob
import yaml



# RE to match the files specify the fold
# e.g home_fold1_train.txt
fold_file_re = re.compile(r'(\w+)_fold(\d+)_(evaluate|train)\.txt')

class Dataset:
    def __init__(self, config):
        self.config = config

# Private Interface
# ===========================================================================

    def _get_training_data(self, audio_files, scene):
        """
        Generate a list tuples to train a system from a list of audio_files.
        params:
            audio_files: [audio_filename] (relative from training)
        return
            samples: [(audio_file, scene, start::float, end::float, label)]
        """
        samples = []
        for audio_file in audio_files:
            code, _ = audio_file.split('.')
            labels_file = code + '.ann'
            labels = self._parse_labels(audio_file, labels_file, scene)
            samples += labels

        return samples

    def _parse_labels(self, audio_file, labels_file, scene):
        """
        Creates a nested dictionary, mapping audio_files to scenes to labels.
        params:
            audio_file: audio filename (relative to training path)
            scene: scene of the label e.g home
            labels_file: labels filename (relative to training path)
        return:
            labels: [(audio_file, scene, start::float, end::float, label)]
        """
        training_path = self.config['dataset']['training']
        audio_file = path.join(training_path, 'audio', scene, audio_file)
        labels_file = path.join(training_path, 'labels', scene, labels_file)
        labels = []
        with open(labels_file, 'r') as f:
            for line in f:
                start, end, label = line.rstrip().split('\t')
                start, end = float(start), float(end)
                labels.append((audio_file, scene, start, end, label))
        return labels


    def _generate_folds(self, folds=4):
        """
        Creates cross validation training data.
        params:
            folds: number of folds to generate
        return:
            generator([(fold_id, scene, training_data, testing_data)
            where...
                training_data: (audio_file, scene, start::float, end::float, label)]
                testing_data: [audio_file]
            The two datasets contain no overlap.
        """
        training_path = self.config['dataset']['training']
        audio_path = path.join(training_path, 'audio')
        scenes = listdir(audio_path)

        for scene in scenes:
            files = listdir(path.join(audio_path, scene))
            splits = np.array_split(files, folds)
            for fold_id in range(folds):
                # remove the current files in being testing out of the training
                training = [ x for (i, x) in enumerate(files) if i != fold_id]
                # Get the data from the files
                training_data = self._get_training_data(training, scene)
                testing = splits[fold_id]
                yield fold_id, scene, training_data, set(testing)

    def _folds_from_file(self, fold_path):
        """
        Create fold data using files in specified path.
        params:
            fold_path: path to fold files.
        return:
            generator([(fold_id, scene, training_data, testing_data)
            where...
                training_data: (audio_file, scene, start::float, end::float, label)]
                testing_data: [audio_file]
            The two datasets contain no overlap.
        """
        fold_dict = defaultdict(lambda: defaultdict(dict))

        # Need to fully create the folds before yielding them
        for fold_file in listdir(fold_path):
            match = fold_file_re.search(fold_file)
            if match:
                scene, fold_id, stage = match.groups()
                fold_dict[scene][fold_id][stage] = fold_file

        for scene in fold_dict:
            folds_count = len(fold_dict[scene].keys())
            # logical to loop through the folds in order
            for fold_id in range(1, folds_count+1):
                fold = fold_dict[scene][str(fold_id)]
                training = path.join(fold_path, fold['train'])
                testing = path.join(fold_path, fold['evaluate'])
                training_data = list(self._get_fold_data(training))
                testing_data = list(self._get_fold_data(testing))

                testing_data = map(lambda x:x[0], testing_data)
                yield fold_id, scene, training_data, set(testing_data)

    def _get_fold_data(self, fold_file, test_file=False):
        """
        Extracts the data from a fold file.
        params:
            fold_file: The name of the fold file relative from root
        return:
            samples: data: (audio_file, scene, start::float, end::float)]
        """
        training_path = self.config['dataset']['training']
        with open(fold_file) as f:
            for line in f:
                line = line.strip().split('\t')
                audio_file, scene, start, end, label = line
                audio_file = path.join(training_path, audio_file)
                yield(audio_file, scene, float(start), float(end), label)

    def _training_files(self, scene):
        """
        Gets the training files for a scene.
        params:
            scene: scene to get training files for
        return:
            files: list of training files
        """
        training_path = self.config['dataset']['training']
        audio_path = path.join(training_path, 'audio')
        files = []
        with open(path.join(audio_path, scene, 'training_order.txt')) as f:
            for line in f:
                files.append(line.strip())

        return files

# Public Interface
# ===========================================================================

    @property
    def training(self):
        """
        Returns ALL the training data in the dataset.
        return:
            training_data: [(audio_file, scene, start::float, end::float, label)]
        """
        training_path = self.config['dataset']['training']
        audio_path = path.join(training_path, 'audio')
        scenes = listdir(audio_path)
        # training_data = []
        for scene in scenes:
            training_files = self._training_files(scene)
            audio_files = listdir(path.join(training_path, 'audio', scene))
            yield scene, self._get_training_data(training_files, scene)

    @property
    def folds(self):
        """
        Generate training data for cross validation testing. Folds of either
        generated automatically or a set of files. This is determined by the
        config file specified.
        return:
            samples: [(fold, scene, start::float, end::float, label)]
        """
        folds = self.config['dataset']['folds']
        if str(folds).isdigit():
            return self._generate_folds(folds)
        else:
            return self._folds_from_file(folds)


    def evaluation(self, scene):
        """
        return:
            files: [full_audio_paths]
        """
        evaluation_path = self.config['dataset']['evaluation']
        audio_path = path.join(evaluation_path, 'audio')
        files = listdir(path.join(audio_path, scene))
        return map(lambda f: path.join(audio_path, scene, f), files)

    def store_results(self, filename, labels, threshold=None):
        """
        Save the labels to a file in the results folder.
        params:
            filename: file to save results to
            labels: { audiofile: [start, end, label] }
        """
        results_path = self.config['dataset']['results']
        experiment_path = path.join(results_path, self.config['experiment_name'], str(threshold))

        print(filename)
        if not os.path.exists(experiment_path):
            print('making directory')
            os.makedirs(experiment_path)


        full_path = path.join(experiment_path, filename)

        with open(full_path, 'w') as f:
            for audio_file, data in labels.items():
                for start, end, label in data:
                    line = '\t'.join([audio_file, str(start), str(end), label])
                    print(line, file=f)

        with open(path.join(experiment_path, 'config.yaml'), 'w+') as f:
            yaml.dump(self.config, f, default_flow_style=False)
