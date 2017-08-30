import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Activation, Dense, Embedding

from keras.utils.visualize_util import plot

from keras.datasets import imdb
# (X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=20000)



class RNN:


    def train(self, features_dict, labels_dict):

        X = None
        for file_name, features in features_dict.items():
            # labels_matrix = np.zeros(features.shape[1]).reshape((1, -1))
            labels_matrix = None


            # print(labels_matrix.shape)
            for event_label, truth_matrix in labels_dict[file_name].items():
                positive_samples = features[:, truth_matrix.T]
                # Add timesteps
                print(positive_samples.shape)

                print(positive_samples)


                if labels_matrix is None:
                    labels_matrix = truth_matrix
                else:
                    labels_matrix = np.vstack((labels_matrix, truth_matrix))

            # Currently bools
            labels_matrix = labels_matrix.T.astype(int)
            print(labels_matrix)
            print(labels_matrix.shape)


            print(' dsjknkj')
            print(features.shape)
            # swwm
            model = Sequential()
            model.add(LSTM(16))
            model.add(Activation('relu'))

            model.compile(loss='categorical_crossentropy',
                            optimizer='rmsprop',
                            metrics=['accuracy'])

            model.fit(features, labels_matrix, nb_epoch=10, batch_size=16)

            # model.fit(features, labels, nb_epoch=10, batch_size=32)

        ndjnj

        return


        for file_name, features in features_dict.items():
            features = features_dict[file_name]
            for event_name, truth_matrix in labels_dict[file_name].items():
                # All the instances of this event in this file
                positive_samples = features[:, truth_matrix.T]
                label_names = np.array(list(labels['data/train/audio/residential_area/a001.wav'].keys()))










        # print(features)
        # print(labels)
        # print(labels.keys())
        #

        label_names = labels_dict.keys()
        # encoder = LabelEncoder()
        # encoder.fit(list(label_names))

        # print(features_dict)



            # for event_label, truth_matrix in event_dict.items():
            #     label_matrix.append(truth_matrix)

            # samples = features.shape[1]
            # label_matrix = []
            #
            # for i in range(samples):
            #     for event in

        dmkdm

        # for label_name in labels['data/train/audio/residential_area/a001.wav']:

        mdkmk
        #
        # X = []
        # Y = []
        #
        # for filename, features = features.items():
        #     labels = labels[features]
        #     X.append(features)
        #     Y.append(labels)
        #
        # model = self.build_model()
        # model.fit(X, Y)

    def classify(self, samples, hop_length):
        pass
