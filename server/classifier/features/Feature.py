import librosa
import os
import wave
import numpy as np
import scipy
import subprocess
import uuid

def load_audio(filename, mono=True, fs=44100):
    """Load audio file into numpy array

    Supports 24-bit wav-format, and flac audio through librosa.

    Parameters
    ----------
    filename:  str
        Path to audio file

    mono : bool
        In case of multi-channel audio, channels are averaged into single channel.
        (Default value=True)

    fs : int > 0 [scalar]
        Target sample rate, if input audio does not fulfil this, audio is resampled.
        (Default value=44100)

    Returns
    -------
    audio_data : numpy.ndarray [shape=(signal_length, channel)]
        Audio

    sample_rate : integer
        Sample rate

    """

    file_base, file_extension = os.path.splitext(filename)
    if file_extension == '.wav':
        print(filename)
        audio_file = wave.open(filename)

        # Audio info
        sample_rate = audio_file.getframerate()
        sample_width = audio_file.getsampwidth()
        number_of_channels = audio_file.getnchannels()
        number_of_frames = audio_file.getnframes()

        # Read raw bytes
        data = audio_file.readframes(number_of_frames)
        audio_file.close()

        # Convert bytes based on sample_width
        num_samples, remainder = divmod(len(data), sample_width * number_of_channels)
        if remainder > 0:
            raise ValueError('The length of data is not a multiple of sample size * number of channels.')
        if sample_width > 4:
            raise ValueError('Sample size cannot be bigger than 4 bytes.')

        if sample_width == 3:
            # 24 bit audio
            a = np.empty((num_samples, number_of_channels, 4), dtype=np.uint8)
            raw_bytes = np.fromstring(data, dtype=np.uint8)
            a[:, :, :sample_width] = raw_bytes.reshape(-1, number_of_channels, sample_width)
            a[:, :, sample_width:] = (a[:, :, sample_width - 1:sample_width] >> 7) * 255
            audio_data = a.view('<i4').reshape(a.shape[:-1]).T
        else:
            # 8 bit samples are stored as unsigned ints; others as signed ints.
            dt_char = 'u' if sample_width == 1 else 'i'
            a = np.fromstring(data, dtype='<%s%d' % (dt_char, sample_width))
            audio_data = a.reshape(-1, number_of_channels).T

        if mono:
            # Down-mix audio
            audio_data = np.mean(audio_data, axis=0)

        # Convert int values into float
        audio_data = audio_data / float(2 ** (sample_width * 8 - 1) + 1)

        # Resample
        if fs != sample_rate:
            audio_data = librosa.core.resample(audio_data, sample_rate, fs)
            sample_rate = fs

        return audio_data, sample_rate

    elif file_extension == '.flac':
        audio_data, sample_rate = librosa.load(filename, sr=fs, mono=mono)

        return audio_data, sample_rate

    return None, None


def vclp(f, fmax, alpha):
    fhigh = 0.8 * fmax
    fhigh = 4800
    f0 = fhigh * min(alpha, 1)

    if f <=  f0/alpha:
        return alpha * f
    else:
        ratio = (fmax - f0) / (fmax - (f0/alpha))
        return fmax - (ratio * (fmax - f))

def get_bin(freq, n_fft, sr):
    bin = np.floor((n_fft + 1) * freq / sr)
    return bin

class Feature:
    # Stores the loaded in files in a dict
    librosa_cache = {}

    def __init__(self):
        self.fs = 44100

    def get_librosa_data(self, file_name):
        if file_name in Feature.librosa_cache:
            return Feature.librosa_cache[file_name]
        else:
            # y, fs = librosa.core.load(file_name, sr=44100, mono=True)
            y, fs = load_audio(file_name, fs=self.fs, mono=True)
            Feature.librosa_cache[file_name] = y, fs
            return y, fs

    def call_yaafe(self, file_name, cmd):
        hash_ = uuid.uuid4().hex
        fs = 44100

        cmd = 'yaafe -r {0} -f "{1}: {2}" {3} -o csv'.format(
                        fs,
                        hash_,
                        cmd,
                        file_name)



        out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        out_filename = file_name + '.' + hash_ + '.csv'

        X = np.genfromtxt(out_filename, delimiter=',', skip_header=5)

        # Remove comments
        # X = X[~np.isnan(X)]
        # Not needed anymore
        os.remove(out_filename)
        return X

    def get_frames(self, y, window_type, win_length, hop_length, n_fft, alpha=None):
        eps = np.spacing(1)
        # Windowing function
        if window_type == 'hamming_asymmetric':
            window = scipy.signal.hamming(n_fft, sym=False)
        elif window_type == 'hamming_symmetric':
            window = scipy.signal.hamming(n_fft, sym=True)
        elif window_type == 'hann_asymmetric':
            window = scipy.signal.hann(n_fft, sym=False)
        elif window_type == 'hann_symmetric':
            window = scipy.signal.hann(n_fft, sym=True)
        else:
            window = None

        frames = librosa.stft(y + eps, n_fft=self.n_fft, win_length=win_length,
                                               hop_length=hop_length,
                                               center=True,
                                               window=window)

        if alpha:
            print('Applying VTLP')
            new_frames = np.zeros_like(frames)
            for i, freq in enumerate(librosa.fft_frequencies(sr=self.fs, n_fft=n_fft)):
                energy = frames[i]
                new_freq = vclp(freq, self.fs / 2, alpha)
                bin = get_bin(new_freq, n_fft, self.fs)
                new_frames[bin] = energy
            return new_frames
        else:
            return frames

    # Must override
    def __call__(self):
        pass
