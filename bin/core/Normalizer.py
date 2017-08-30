import numpy as np

class Normalizer:
    def __init__(self, feature_matrix=None):
        self.N = 0
        self.S1 = 0
        self.S2 = 0

        if feature_matrix:
            self.add(feature_matrix)
            self.finalize()

    def add(self, feature_matrix):
        # for feature_matrix in feature_matrix_list:
        #     print(feature_matrix.shape)
        self.N += feature_matrix.shape[1]
        self.S1 += np.sum(feature_matrix, axis=1)
        self.S2 += np.sum(feature_matrix ** 2, axis=1)

    def finalize(self):
        N, S1, S2 = self.N, self.S1, self.S2
        mean = S1 / N
        std = np.sqrt((N * S2 - (S1**2)) / (N * (N - 1)))
        std = np.nan_to_num(std)

        self.mean = np.reshape(mean, [1, -1]).T
        self.std = np.reshape(std, [1, -1]).T


    def normalize(self, feature_matrix):
        print('MEAN: ', self.mean)
        return (feature_matrix - self.mean) / self.std
