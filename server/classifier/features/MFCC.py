import librosa
from .Feature import Feature
import numpy as np
import scipy

class MFCC(Feature):
    def __init__(self,
                    window='hamming_asymmetric',
                    n_mfcc=20,
                    n_mels=40,
                    n_fft=2048,
                    fmin=0,
                    fmax=22050,
                    htk=False,
                    delta=None,
                    acceleration=None):
        super().__init__()
        self.window = window
        self.n_mfcc = n_mfcc
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.fmin = fmin
        self.fmax = fmax
        self.htk = htk
        self.delta = delta
        self.acceleration = acceleration


    def __call__(self, file_name, win_duration, hop_duration):
        y, fs = self.get_librosa_data(file_name)
        win_length = int(win_duration * fs)
        hop_length = int(hop_duration * fs)

        frames = self.get_frames(y,
                win_length=win_length,
                hop_length=hop_length,
                n_fft=self.n_fft,
                window_type=self.window
        )

        power_spectrogram = np.abs(frames)**2
        mel_basis = librosa.filters.mel(sr=fs,
                                        n_fft=self.n_fft,
                                        n_mels=self.n_mels,
                                        fmin=self.fmin,
                                        fmax=self.fmax,
                                        htk=self.htk)

        mel_spectrum = np.dot(mel_basis, power_spectrogram)
        mfcc = librosa.feature.mfcc(S=librosa.logamplitude(mel_spectrum),
                                        n_mfcc=self.n_mfcc)


        # Collect the feature matrix
        feature_matrix = mfcc

        # if not self.include_mfcc0:
        #     # Omit mfcc0
        #     feature_matrix = feature_matrix[1:, :]

        return feature_matrix
