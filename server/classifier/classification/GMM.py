import math
import numpy as np

from collections import OrderedDict
from sklearn import mixture


class GMM:

    def __init__(self, *, model, smoothing_window):
        self.models = {}
        self.classifier_params = model
        self.smoothing_window = smoothing_window
        # self.threshold = threshold

    def train(self, features_dict, labels_dict):
        """
        params:
            features_dict[audio_file] = feature_vect
            labels_dict[audio_file][event_label] = truth_matrix
        """
        # Stores all instances of an event
        positive_data = OrderedDict()
        # Stores all instances of other events
        negative_data = OrderedDict()

        for file_name, features in features_dict.items():
            for event_name, truth_matrix in labels_dict[file_name].items():
                # All the instances of this event in this file
                positive_samples = features[:, truth_matrix.T]
                # All the instances of other events in this file
                negative_samples = features[:, ~truth_matrix.T]

                # If we've seen this event before, concate the samples to
                # the previously seen events.
                if event_name in positive_data:
                    positive_data[event_name] = np.hstack(
                        (positive_data[event_name], positive_samples)
                    )
                else:
                    positive_data[event_name] = positive_samples

                if event_name in negative_data:
                    negative_data[event_name] = np.hstack(
                        (negative_data[event_name], negative_samples)
                    )
                else:
                    negative_data[event_name] = negative_samples

        # Store all the models of the events
        # models[event_label]['positive'|'negative'] = GMM
        models = {}
        classifier_params = self.classifier_params

        for event_label in positive_data:
            print(event_label)
            print(positive_data[event_label].shape)
            print(classifier_params)
            models[event_label] = {}
            models[event_label]['positive'] = mixture.GMM(**classifier_params).fit(positive_data[event_label].T)
            print(models[event_label]['positive'].weights_)
            models[event_label]['negative'] = mixture.GMM(**classifier_params).fit(negative_data[event_label].T)

        self.models = models

    def classify(self, samples, hop_length, threshold):
        """
        Classify a samples matrix.
        params:
            samples: np.array(samples, shape=(len(features), len(no_samples)))
            hop_length: amount the window slides by in seconds
        return:
            Generator([event_label, event_activity])
            where...
                events labels is a truth matrix, stating whethere that event
                is present or not for that frame.
        """
        samples = samples.T
        smoothing_window = int(self.smoothing_window / hop_length)

        for event_label in self.models:
            model = self.models[event_label]
            positive = model['positive'].score_samples(samples)[0]
            negative = model['negative'].score_samples(samples)[0]

            # Accumulate likelihoods sliding a window.
            for stop_id in range(0, samples.shape[0]):
                start_id = stop_id - smoothing_window
                if start_id < 0:
                    start_id = 0
                positive[start_id] = sum(positive[start_id:stop_id])
                negative[start_id] = sum(negative[start_id:stop_id])
            likelihood_ratio = positive - negative
            event_activity = likelihood_ratio > threshold
            yield event_label, event_activity
