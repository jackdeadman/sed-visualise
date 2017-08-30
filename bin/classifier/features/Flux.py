from .Feature import Feature
import numpy as np
import os
import subprocess


class Flux(Feature):

    def __init__(self, n_fft, window):
        super().__init__()
        self.n_fft = n_fft
        self.window = window

    def __call__(self, file_name, win_duration, hop_duration):
        win_length = int(win_duration * self.fs)
        hop_length = int(hop_duration * self.fs)

        cmd = 'SpectralFlux FFTLength={n_fft} FFTWindow={window} FluxSupport=All blockSize={win_length} stepSize={hop_length}'.format(
                    n_fft=self.n_fft, window='Hamming', win_length=win_length, hop_length=hop_length
        )

        features = self.call_yaafe(file_name, cmd)
        features = features.reshape((1, -1))
        print(features.shape)
        return features


        # SpectralFlux FFTLength=0  FFTWindow=Hanning  FluxSupport=All  blockSize=1024  stepSize=512
        # > yaafe -r 44100 -f "mfcc: MFCC blockSize=1024 stepSize=512" test.wav
        fs = 44100
        win_length = int(win_duration * fs)
        hop_length = int(hop_duration * fs)
        print(hop_length)

        cmd = 'yaafe -r {0} -f "flux: SpectralFlux FFTLength={1} FFTWindow={2} FluxSupport=All blockSize={3} stepSize={4}" {5} -o csv'.format(
                        fs,
                        self.n_fft,
                        'Hanning',
                        win_length,
                        hop_length,
                        file_name)


        out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        out_filename = file_name + '.flux.csv'
        X = np.genfromtxt(out_filename, delimiter=',')
        # Remove comments
        X = X[~np.isnan(X)]
        print(X)
        X = X.reshape((1, -1))
        print(X)
        # Not needed anymore
        os.remove(out_filename)
        return X
        print(X.shape)
        # out = os.system(cmd)
        print(cmd)
        print(out)
        sxnj


    def __call__old(self, file_name, win_duration, hop_duration):

        y, fs = self.get_librosa_data(file_name)
        win_length = int(win_duration * fs)
        hop_length = int(hop_duration * fs)

        frames = self.get_frames(y,
                win_length=win_length,
                hop_length=hop_length,
                n_fft=self.n_fft,
                window_type=self.window
        )
        X = np.abs(frames)
        # compute the spectral flux as the sum of square distances:
        sumX = np.sum(X, axis=0)
        prevX = np.zeros(X.shape)
        prevX[:,1:] = X[:, -1:]
        prevX[:, 0] = X[:, 0]

        # sumX = np.sum(X + eps)
        sumPrevX = np.sum(prevX)
        F = np.sum((X / sumX - prevX/sumPrevX) ** 2, axis=0)
        F = F.reshape((1,-1))
        print(F)
        return F
