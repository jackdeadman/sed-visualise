import librosa
from .Feature import Feature
import numpy as np
import scipy

class Rolloff(Feature):

    def __init__(self, n_fft, window):
        super().__init__()
        self.n_fft = n_fft
        self.window = window

    def __call__(self, file_name, win_duration, hop_duration):
        y, sr = self.get_librosa_data(file_name)
        hop_length = int(hop_duration * sr)
        win_length = int(win_duration * sr)

        frames = self.get_frames(y,
                win_length=win_length,
                hop_length=hop_length,
                n_fft=self.n_fft,
                window_type=self.window
        )

        rolloff = librosa.feature.spectral_rolloff(S=np.abs(frames), sr=sr)
        print('rolloff', rolloff.shape)
        return rolloff
