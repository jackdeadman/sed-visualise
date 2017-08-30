from .Feature import Feature
import numpy as np
import os
import subprocess


class Sharpness(Feature):

    def __init__(self, n_fft, window):
        super().__init__()
        self.n_fft = n_fft
        self.window = window

    def __call__(self, file_name, win_duration, hop_duration):
        win_length = int(win_duration * self.fs)
        hop_length = int(hop_duration * self.fs)

        cmd = 'PerceptualSharpness FFTLength={n_fft} FFTWindow={window} blockSize={win_length} stepSize={hop_length}'.format(
                    n_fft=self.n_fft, window='Hamming', win_length=win_length, hop_length=hop_length
        )

        features = self.call_yaafe(file_name, cmd)
        features = features.reshape((1, -1))
        print(features.shape)
        return features
