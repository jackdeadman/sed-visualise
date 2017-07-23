import sed_eval
from sed_eval.util.event_list import EventList
from sed_eval.io import load_event_list
from sed_eval.sound_event import SegmentBasedMetrics
from sed_eval.sound_event import EventBasedMetrics

from os import listdir
from os import path
import os
from .Dataset import Dataset
import yaml

from shutil import rmtree

from collections import OrderedDict

def score(file_list):
    data = []
    all_data = sed_eval.util.event_list.EventList()
    for file_pair in file_list:
        reference_event_list = sed_eval.io.load_event_list(file_pair['reference_file'])
        estimated_event_list = sed_eval.io.load_event_list(file_pair['estimated_file'])
        data.append({'reference_event_list': reference_event_list,
                     'estimated_event_list': estimated_event_list})
        all_data += reference_event_list
    event_labels = all_data.unique_event_labels


    # Create metrics classes, define parameters
    # print(event_labels)
    # print(data)
    # xjn
    segment_based_metrics = sed_eval.sound_event.SegmentBasedMetrics(event_label_list=event_labels,
                                                                     time_resolution=1)
    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(event_label_list=event_labels, t_collar=0.2)

    # Go through files
    for file_pair in data:
        # print(file_pair)
        segment_based_metrics.evaluate(file_pair['reference_event_list'],
                                       file_pair['estimated_event_list'])
        event_based_metrics.evaluate(file_pair['reference_event_list'],
                                     file_pair['estimated_event_list'])

    # Get only certain metrics
    # overall_segment_based_metrics = segment_based_metrics.results_overall_metrics()
    # print("Accuracy:", overall_segment_based_metrics['accuracy']['accuracy'])

    # Or print all metrics as reports
    return segment_based_metrics

    # print(overall_segment_based_metrics['f_measure']['f_measure'])
    # print(event_based_metrics)



def get_files_fold(fold_file):
    files = set()
    with open(fold_file) as f:
        for line in f:
            files.add(line.split('\t')[0])

    return files

def score_folders(reference_path, estimated_path):
    results_dict = OrderedDict()
    for scene in ['home', 'residential_area']:
        results = score_folders_scene(scene, reference_path, estimated_path)
        results_dict[scene] = results
        # results_list.append(results)

    print('===== OVERALL =====')
    print('F-Score'.upper())
    scores = 0
    for scene, results in results_dict.items():
        print('\t', end='')
        print(scene, end=': ')
        f_score = results.overall_f_measure()['f_measure']
        scores += f_score
        print('{0:.1f}%'.format(f_score*100))
    print('\tAverage: ', end='')
    print('{0:.1f}%'.format((scores*100) / len(results_dict.keys())))

    print('error rate'.upper())
    scores = 0
    for scene, results in results_dict.items():
        print('\t', end='')
        print(scene, end=': ')
        er = results.overall_error_rate()['error_rate']
        scores += er
        print('{0:.2f}'.format(er))

    print('\tAverage: ', end='')
    print('{0:.2f}'.format((scores) / len(results_dict.keys())))



    for scene, results in results_dict.items():
        print(scene.upper())
        print(results)

def score_folders_scene(scene, reference_path, estimated_path):
    # reference_path = 'data/evaluation_setup'
    reference_files = [f for f in listdir(reference_path)
                                        if f.endswith('evaluate.txt')
                                        and scene in f]



    # estimated_path = 'results'
    # estimated_path = 'results'
    estimated_files = [f for f in listdir(estimated_path)
                                        if f.endswith('results.txt')
                                        and scene in f]

    reference_files.sort()
    estimated_files.sort()
    # Create data list
    data_list = []
    lines = {}
    reference_path_sep = path.join(estimated_path, 'separate')

    for reference_file, estimated_file in zip(reference_files, estimated_files):
        fold_file = path.join(reference_path, reference_file)
        files = get_files_fold(fold_file)

        # print(reference_path_sep)
        if not os.path.exists(reference_path_sep):
            os.makedirs(reference_path_sep)

        for file_ in files:
            audiofile = file_.split('/')[-1]
            new_filename = audiofile + '_' +  estimated_file

            with open(path.join(estimated_path, estimated_file)) as f:
                with open(path.join(reference_path_sep, new_filename), 'w+') as g:
                    for line in f:
                        parts = line.split('\t')
                        actualfile =  parts[0].split('/')[-1]
                        if audiofile == actualfile:
                            print(str(line), file=g, end='')

            code = audiofile.split('.')[0]

            data_list.append({
                'reference_file': path.join('data/evaluation/labels/'+scene, code+'.ann'),
                'estimated_file': path.join(reference_path_sep, new_filename)
            });
        # xmks
        # audio_file = path.join('data/evaluation/audio', 'home', file_)

        # result_filename = path.join('data/evaluation_setup_changed', estimated_file)
        # print(result_filename)
        # results = []
        # if path.isfile(result_filename):
        #     print('reading...')
        #     with open(result_filename, 'rt') as f:
        #         for row in csv.reader(f, delimiter='\t'):
        #             results.append(row)

        # with open('configs/train/baseline.yaml') as f:
        #     config = yaml.load(f)
        # dataset = Dataset(config)

        '''
        for fold_id, scene, _, testing in dataset.folds:
            current_file_results = []
            for file_ in testing:
                audio_file = path.join('data/evaluation/audio', scene, file_)
                for result_line in results:
                    if len(result_line) != 0 and result_line[0] == file_:
                        current_file_results.append(
                            {'file': result_line[0],
                             'event_onset': float(result_line[1]),
                             'event_offset': float(result_line[2]),
                             'event_label': result_line[3].rstrip()
                             }
                        )
                # else:
                    # print 'Skip'
                    # print result_line
                code, ext = file_.split('.')
                label_file = code + '.ann'
                meta = path.join('data/evaluation/labels', scene, label_file)
                # print current_file_results
                # print meta
                # print(current_file_results)
                sed_eval.sound_event.SegmentBasedMetrics.evaluate(system_output=current_file_results)
                sed_eval.sound_event.EventBasedMetrics.evaluate(system_output=current_file_results)
        '''

        # print(reference_file, estimated_file)
        # data_list.append({
        #     'reference_file': path.join(reference_path, reference_file),
        #     'estimated_file': path.join(estimated_path, estimated_file)
        # });
        #
        #
        # with open(path.join(reference_path, reference_file), 'r') as f:
        #     for line in f:
        #         fi, scene, start, end, label = line.strip().split('\t')
        #         if label not in lines:
        #             lines[label] = 0
        #         lines[label] += 1

    result = score(data_list)
    rmtree(reference_path_sep)
    return result
