from os import path, getcwd

# Classifier Stuff
from core.SoundEventDetector import SoundEventDetector
from core.Dataset import Dataset

from classifier.features.MFCC import MFCC
from classifier.features.Centroid import Centroid
from classifier.features.Energy import Energy
from classifier.features.Flux import Flux
from classifier.features.Rolloff import Rolloff
from classifier.features.Sharpness import Sharpness
from classifier.features.Slope import Slope
from classifier.features.Spread import Spread
from classifier.features.ZeroCrossingRate import ZeroCrossingRate


from classifier.classification.GMM import GMM
from classifier.post_processing.CombineEvents import CombineEvents
from classifier.post_processing.RemoveShortEvents import RemoveShortEvents

import pickle

def save_file(filename, obj):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, 'wb') as f:
        pickle.dump(obj=obj, file=f)

def load_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def create_classifier(features, scene, norm_path, model_path):
    print(features)
    feature_objs = []

    if 'mfcc' in features:
        mfcc = MFCC(
            window='hamming_asymmetric',
            n_mfcc=20,
            n_mels=40,
            n_fft=2048,
            fmin=0,
            fmax=22050,
            htk=False,
            delta=9,
            acceleration=9
        )
        feature_objs.append(mfcc)

    feature_classes = {
        'centroid': Centroid,
        'energy': Energy,
        'flux': Flux,
        'rolloff': Rolloff,
        'slope': Slope,
        'sharpness': Sharpness,
        'spread': Spread,
        'zcr': ZeroCrossingRate
    }


    time_domain = {'zcr', 'energy'}

    for feature_name in features:
        if feature_name in feature_classes:
            Feature = feature_classes[feature_name]

            if feature_name in time_domain:
                feature_objs.append(Feature())
            else:
                feature_objs.append(Feature(
                    n_fft=2048,
                    window='hamming_asymmetric'
                ))

    gmm = GMM(
        model={
            'n_components': 8,
            'covariance_type': 'diag',
            'random_state': 0,
            'tol': 0.001,
            'min_covar': 0.001,
            'n_iter': 40,
            'n_init': 1,
            'params': 'wmc',
            'init_params': 'wmc'
        },
        smoothing_window=1
    )
    print(features)
    system = SoundEventDetector(
        features=feature_objs,
        post_processors=[
                RemoveShortEvents(minimum_event_duration=0.1),
                CombineEvents(minimum_event_gap=0.1)
        ],
        classifier=gmm,
        win_duration=0.04,
        hop_duration=0.02,
        use_deltas=True,
        drop_first_feature=True,
        vtlp=False
    )

    data_path = 'server/classifier/sed-data/'
    normalizers_path = path.join(getcwd(), data_path, 'normalizers', norm_path, 'normalizers.pkl')
    print(normalizers_path)
    print(getcwd())
    normalizers = load_file(normalizers_path)
    print(normalizers)
    models_path = path.join(data_path, 'models', model_path, 'models.pkl')
    print(models_path)
    models = load_file(models_path)

    system.normalizer = normalizers[scene][2]
    system.models = models[scene][2]
    return system
