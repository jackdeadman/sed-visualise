from collections import OrderedDict
import math
import numpy as np
import librosa

import pickle

from sklearn import decomposition

from core.Normalizer import Normalizer
from classifier.utils.unique import unique

from classifier.features.MFCC import MFCC

class SoundEventDetector:
    """
    Joins all the components of a sound event detection system together
    params:
        features: lists of Feature instances
        classifier: Classifier instance
        post_processors: list of post_processors
        win_duration: length of a window in seconds
        hop_duration: length of the hop between windows in seconds
    """
    def __init__(self,
                features=None,
                classifier=None,
                post_processors=None,
                win_duration=0.04,
                hop_duration=0.02,
                pca=None,
                use_deltas=None,
                pca_components=20,
                drop_first_feature=True,
                vtlp=None
                ):

        # Setting default like this as default args of [] causing issues
        self.features = features or []
        self.post_processors = post_processors or []
        print('VTLP', vtlp)
        if classifier is None:
            raise ValueError('classifer must be defined.')

        # Set remaining attributes
        self.classifier = classifier
        self.normalizer = Normalizer()
        self.training_data = {}
        self.win_duration = win_duration
        self.hop_duration = hop_duration
        self.pca_components = None
        self.pca = None
        self.use_deltas = use_deltas
        self.drop_first_feature = drop_first_feature
        self.vtlp = vtlp
        if pca:
            self.pca_components = pca_components
            # self.pca = decomposition.PCA(n_components=pca_components)

# Private Interface
# ===========================================================================

    def _create_feature_vect(self, audio):
        feature_vect = None
        for feature in self.features:
            # Combine the feature vectors together
            features = feature(audio, self.win_duration, self.hop_duration)

            if feature_vect is None:
                feature_vect = features
            else:
                # print(feature_vect.shape)
                # print(features.shape)
                feature_vect = np.vstack((feature_vect, features))

        features = feature_vect
        if self.use_deltas:
            delta = 9
            acceleration = 9


            # Delta coefficients
            mfcc_delta = librosa.feature.delta(feature_vect, width=delta)

            # Add Delta Coefficients to feature matrix
            features = np.vstack((features, mfcc_delta))

            # Acceleration coefficients (aka delta delta)
            mfcc_delta2 = librosa.feature.delta(feature_vect, order=2, width=acceleration)

            # Add Acceleration Coefficients to feature matrix
            features = np.vstack((features, mfcc_delta2))

        if self.drop_first_feature:
            features = features[1:, :]
        return features

    def _extract_features(self, audio_paths, use_vtlp=True):
        """
        Creates a dict of audio files mapping to features
        params:
            audio_paths: [audio_path]
        return:
            feature_dict[audio_file] = feature_vect
            where...
                feature_vect = np.array(features, shape=(len(features), len(samples)))
        """
        feature_dict = OrderedDict()
        print('--------UNQIUE---------')
        # print(unique(audio_paths))
        for audio in unique(audio_paths):
            feature_dict[audio] = self._create_feature_vect(audio)

        return feature_dict


    # labels[audio_file][event] = matrix
    def _extract_labels(self, features_dict, training):
        """
        Creates a label dictionary from training data, featue vector is needed
        to create the truth matrix.
        params:
            features_dict[audio_file] = feature_vect
            training = [(audiofile, scene, start, end, label)]
        reutrn:
            labels_dict[audio_file][event_label] = truth_matrix
        """
        labels_dict = OrderedDict()
        for audio_file, scene, start, end, label in training:
            # print(audio_file)
            if audio_file not in labels_dict:
                labels_dict[audio_file] = OrderedDict()

            features = features_dict[audio_file]
            # print(features.shape)
            no_samples = features.shape[1]
            # print(no_samples)

            if label in labels_dict[audio_file]:
                # If we've seen this file before, continue where
                # we left off
                truth_matrix = labels_dict[audio_file][label]
            else:
                # Start with all false if we have not seen the file
                truth_matrix = np.zeros((features.shape[1]), dtype=bool)

            # Add in trues where the event is present
            start_frame = int(math.floor(start / self.hop_duration))
            stop_frame = int(math.ceil(end / self.hop_duration))

            truth_matrix[start_frame:stop_frame] = True
            labels_dict[audio_file][label] = truth_matrix

        return labels_dict

    def _apply_normalize(self, training_data):
        """
        Normalize the features based on the normalizer created from training data
        """
        new_data = OrderedDict()
        for filename, feature_matrix in training_data.items():
            new_data[filename] = self.normalizer.normalize(feature_matrix)
        return new_data

    # Credit: Toni Heittola
    def _contiguous_regions(self, activity_array):
        # Find the changes in the activity_array
        change_indices = np.diff(activity_array).nonzero()[0]
        # print((activity_array == 1).sum())
        # print((activity_array == 0).sum())

        # Shift change_index with one, focus on frame after the change.
        change_indices += 1

        if activity_array[0]:
            # If the first element of activity_array is True add 0 at the beginning
            change_indices = np.r_[0, change_indices]

        if activity_array[-1]:
            # If the last element of activity_array is True, add the length of the array
            change_indices = np.r_[change_indices, activity_array.size]

        # Reshape the result into two columns
        return change_indices.reshape((-1, 2))

# Public Interface
# ===========================================================================

    def train(self):
        """
        Train the classifier on the training data already provided.
        """
        self.training_data = self._apply_normalize(self.training_data)
        # print(self.training_labels['data/train/audio/home/a034.wav']['object impact'].sum())
        self.classifier.train(self.training_data, self.training_labels)

    def create_normalizer(self):
        """
        Create the normalizer for the training data provided.
        """
        normalizer = Normalizer()
        for feature_matrix in self.training_data.values():
            normalizer.add(feature_matrix)
        normalizer.finalize()
        self.normalizer = normalizer


    def create_pca_basis(self, training_data, components=40):
        # Easy to handle
        training_data = training_data.T
        mean = training_data.mean(axis=0)
        # Center
        training_data = training_data - mean
        cov = np.cov(training_data, rowvar=False)
        values, eig = np.linalg.eig(cov)
        print(eig.shape)
        # Sort
        indices = np.argsort(values)[::-1]
        basis = np.array(eig[:, indices])

        # Drop components
        print('Basis before: ')
        print(basis.shape)
        return basis[:, :components], mean

    def vocal_tube_length_perturbation(self, freqs):
        a = np.random.uniform(0.9, 1.1)
        fmax = 22050
        S = 44100
        print('VOCAL TUBE FACTOR', a)
        capped = min(a, 1)

        for i, freq in enumerate(freqs):
            for j, f in enumerate(freq):
                if f <= fmax*(capped/a):
                    freqs[i][j] = f*a
                else:
                    middle = S/2 - fmax*capped
                    freqs[i][j] = S/2 - middle*(S/2 - f)

        return freqs

    def add_training(self, training):
        """
        Add data to the training set.
        params:
            training: [(audio_file, scene, start::float, end::float, label)]
        """
        features = self._extract_features(map(lambda a:a[0], training))

        if self.pca_components:
            # pca = decomposition.PCA(n_components=self.pca_components)
            all_training = None

            for filename, feature_matrix in features.items():
                if all_training is not None:
                    all_training = np.hstack((all_training, feature_matrix))
                else:
                    all_training = feature_matrix

            basis, mean = self.create_pca_basis(all_training, self.pca_components)
            # project
            for filename, feature_matrix in features.items():
                feature_matrix = feature_matrix.T
                projected = np.dot(feature_matrix - mean, basis)
                features[filename] = projected.T

            self.pca = (basis, mean)

        # for filename, feature_matrix in features.items():
        #     if type(feature_matrix) != list:
        #         features[filename] = [feature_matrix]

        self.training_data = features
        self.training_labels = self._extract_labels(features, training)

    def add_testing(self, testing_files):
        features = self._extract_features(testing_files, False)
        if self.pca:
            basis, mean = self.pca
            for filename, feature_matrix in features.items():
                features[filename] = np.dot((feature_matrix.T - mean), basis).T

        features = self._apply_normalize(features)
        self.testing_data = features

    def classify(self, threshold):
        """
        Classify a list of audio files.
        parmas:
            files: [audio_files]
        """
        features_dict = self.testing_data
        guessed_labels = {}

        for file_name, features in features_dict.items():
            print(file_name)

            guesses = []
            for event_label, event_activity in self.classifier.classify(features, self.hop_duration, threshold):
                if event_activity.any():
                    event_segments = self._contiguous_regions(event_activity) * self.hop_duration
                    for post_processor in self.post_processors:
                        event_segments = post_processor(event_segments)

                    for start, end in event_segments:
                        guesses.append((start, end, event_label))

            guessed_labels[file_name] = guesses

        return guessed_labels

    @property
    def models(self):
        return self.classifier.models

    @models.setter
    def models(self, models):
        self.classifier.models = models

    def reset(self):
        """
        Restore the system to a fresh start
        """
        self.classifier.models = {}
        self.training_data = None
        self.training_labels = None
        self.testing_data = None
        self.normalizer = None
        self.pca = None
