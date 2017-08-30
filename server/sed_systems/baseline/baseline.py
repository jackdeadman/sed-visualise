# Library
from modules.classifier import Classifier

# from sound_event_detector.core.sound_event_detector import SoundEventDetector
# from sound_event_detector.classifier.GMM import GMM
# from sound_event_detector.features.MFCC import MFCC

# from sound_event_detector.core.sound_event_detector import SoundEventDetector
# from sound_event_detector.classification.gmm import GMM
# from sound_event_detector.features.mfcc import MFCC

class Baseline(Classifier):
    
    @property
    def use_caching(self):
        return False
    
    @property
    def config(self):
        return {
            'id': 'baseline',
            'title': 'DCASE 2016 Baseline System',
            'description': 'No description provided.'
        }

    def setup(self):
        """
        Setup the classifier e.g load models.
        This is called only once on the server startup,
        unless use_caching=False.
        """
        return
        mfcc = MFCC(window='hamming_asymmetric', n_mfcc=20,
                    n_mels=40, n_fft=2048, fmin=0, fmax=22050,
                    htk=False, delta=9, acceleration=9)

        gmm = GMM(
        model={
            'n_components': config['classifier']['components'],
            'covariance_type': 'diag',
            'random_state': 0,
            'tol': 0.001,
            'min_covar': 0.001,
            'n_iter': 40,
            'n_init': 1,
            'params': 'wmc',
            'init_params': 'wmc'
        }, smoothing_window=1)

        classifier = SoundEventDetector(
                    features=[mfcc], classifier=gmm,
                    win_duration=0.04, hop_duration=0.02)
        
        with open('path/to/models', 'rb') as f:
            classified.models = pickle.load(f)

    def classify(self, audio):
        """
        Run the classifer using the loaded models.
        @param audio: Audio object of the file being classified
        @return numpy array, location to text file or text file object
        """
        return '\n'.join([
            '0\t10\tObject Impact',
            '0\t20\tObject Impact1',
            '30\t35\tObject Impact2'
        ])
        return '\n'.join(['0 \t 1 \ testing'])
        return self.classifier.classify(audio.file_path, 160)
