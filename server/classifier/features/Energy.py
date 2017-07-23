import librosa
from .Feature import Feature
import numpy as np
import scipy

class Energy(Feature):

    def __init__(self):
        super().__init__()

    def __call__(self, file_name, win_duration, hop_duration):
        y, sr = self.get_librosa_data(file_name)
        hop_length = int(hop_duration * sr)
        win_length = int(win_duration * sr)

        rmse = librosa.feature.rmse(y, hop_length=hop_length, n_fft=win_length)
        # cent2 = librosa.feature.spectral_centroid(y=y, n_fft=2048, sr=sr, hop_length=hop_length)
        return rmse
