# Python Dependencies
import argparse
import sys
import os
from os import path
import pickle

from collections import defaultdict

# Library Dependencies
import numpy as np
import yaml

# Core Dependencies
from core.Dataset import Dataset
from core.SoundEventDetector import SoundEventDetector

#Components
from classification.GMM import GMM

from features.AutoCorrelation import AutoCorrelation
from features.Centroid import Centroid
from features.Energy import Energy
from features.Flux import Flux
from features.MFCC import MFCC
from features.Rolloff import Rolloff
from features.Slope import Slope
from features.Sharpness import Sharpness
from features.Spread import Spread
from features.ZeroCrossingRate import ZeroCrossingRate

from post_processing.CombineEvents import CombineEvents
from post_processing.RemoveShortEvents import RemoveShortEvents

# from core.Evaluation import DCASE2016_EventDetection_SegmentBasedMetrics

def save_file(filename, obj):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, 'wb') as f:
        pickle.dump(obj=obj, file=f)

def load_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def main(args):
    with open(args.config) as f:
        config = yaml.load(f)

    if args.seed:
        seed = int(args.seed)
    elif 'seed' in config:
        seed = int(config['seed'])
    else:
        seed = 123456

    if args.cache:
        config['cache-directory'] = args.cache
    if args.results:
        config['dataset']['results'] = args.results

    if args.setup:
        config['dataset']['folds'] = args.setup

    if ('augmentation' not in config ) or ('vtlp' not in config['augmentation']):
        config['augmentation'] = {}
        config['augmentation']['vtlp'] = False

    threshold = False
    if 'tasks' not in config:
        config['tasks'] = {}
    if 'use_cache' not in config:
        config['use_cache'] = {}

    if 'use_deltas' not in config:
        config['use_deltas'] = True

    if args.mode:
        threshold = False
        if args.mode == 'classify':
            config['tasks']['extract_features'] = False
            config['tasks']['train'] = True
            config['tasks']['classify'] = True

            config['use_cache']['extract_features'] = True
            config['use_cache']['train'] = False

        elif args.mode == 'threshold':
            config['tasks']['extract_features'] = False
            config['tasks']['train'] = False
            config['tasks']['classify'] = True

            config['use_cache']['extract_features'] = True
            config['use_cache']['train'] = True
            threshold = True

        elif args.mode == 'train':
            config['tasks']['extract_features'] = False
            config['tasks']['train'] = True
            config['tasks']['classify'] = False

            config['use_cache']['extract_features'] = True
            config['use_cache']['train'] = False

        elif args.mode == 'extract_features':
            config['tasks']['extract_features'] = True
            config['tasks']['train'] = False
            config['tasks']['classify'] = False

            config['use_cache']['extract_features'] = False
            config['use_cache']['train'] = False

        elif args.mode == 'full':
            config['tasks']['extract_features'] = True
            config['tasks']['train'] = True
            config['tasks']['classify'] = True

            config['use_cache']['extract_features'] = False
            config['use_cache']['train'] = False
        else:
            raise ValueError('Mode not found: %s' % args.mode)


    print('Mode: %s' % (args.mode or 'Default'))

    np.random.seed(seed)
    # development = len(sys.argv) > 1 and sys.argv[1] == '--development'
    development = True
    # TODO add better command line passing
    dataset = Dataset(config)

    feature_classes = {
        'auto_correlation': AutoCorrelation,
        'centroid': Centroid,
        'energy': Energy,
        'flux': Flux,
        'rolloff': Rolloff,
        'slope': Slope,
        'sharpness': Sharpness,
        'spread': Spread,
        'zcr': ZeroCrossingRate
    }

    features = []

    if config['features']['mfcc']:
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
        features.append(mfcc)

    time_domain = {'zcr', 'energy'}

    for feature_name, feature_bool in config['features'].items():
        if feature_bool and feature_name in feature_classes:
            Feature = feature_classes[feature_name]

            if feature_name in time_domain:
                features.append(Feature())
            else:
                features.append(Feature(
                    n_fft=2048,
                    window='hamming_asymmetric'
                ))
    print(features)
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
        },
        smoothing_window=1
    )

    use_pca = 'pca' in config
    pca_components = None
    if use_pca:
        pca_components = config['pca']['pca_components']
        print('Using pca: ', pca_components)

    system = SoundEventDetector(
                features=features,
                post_processors=[
                        RemoveShortEvents(minimum_event_duration=0.1),
                        CombineEvents(minimum_event_gap=0.1)
                ],
                classifier=gmm,
                # classifier=rnn,
                win_duration=0.04,
                hop_duration=0.02,
                pca=use_pca,
                use_deltas=config['use_deltas'],
                pca_components=pca_components,
                drop_first_feature=True,
                vtlp=config['augmentation']['vtlp']
            )


    if development:
        print('DEVELOPMENT MODE')
        normalizers = {}
        models = {}
        pcas = {}
        directory = path.join(config['cache-directory'], 'models', config['experiment_name'])
        features_directory = path.join(config['cache-directory'], 'features', config['features-directory'])

        if config['use_cache']['extract_features']:
            normalizers = load_file(path.join(features_directory, 'normalizers.pkl'))
            if use_pca:
                pcas = load_file(path.join(features_directory, 'pcas.pkl'))

        # Save the normalizers and models
        if not os.path.exists(directory):
            os.makedirs(directory)

        for fold_id, scene, training, _ in dataset.folds:
            print('Fold: ', fold_id)
            training_data_file = '%s-%s-training_data.pkl' % (scene, fold_id)
            training_labels_file = '%s-%s-training_labels.pkl' % (scene, fold_id)

            training_data_file_full = path.join(features_directory, training_data_file)
            training_labels_full = path.join(features_directory, training_labels_file)

            if config['tasks']['extract_features']:
                system.add_training(training)
                system.create_normalizer()
                save_file(training_data_file_full, system.training_data)
                save_file(training_labels_full, system.training_labels)

            if config['use_cache']['extract_features']:
                system.training_data = load_file(training_data_file_full)
                system.training_labels = load_file(training_labels_full)
                system.normalizer = normalizers[scene][fold_id]
                if use_pca:
                    system.pca = pcas[scene][fold_id]

            print('Training added')
            if config['tasks']['train']:
                system.train()

            if scene not in models:
                models[scene] = {}

            if scene not in normalizers:
                normalizers[scene] = {}

            if scene not in pcas:
                pcas[scene] = {}

            normalizers[scene][fold_id] = system.normalizer
            models[scene][fold_id] = system.models
            pcas[scene][fold_id] = system.pca
            system.reset()

        if not config['use_cache']['extract_features']:
            # Should have been defined from training so save it
            save_file(path.join(features_directory, 'normalizers.pkl'), normalizers)
            if use_pca:
                save_file(path.join(features_directory, 'pcas.pkl'), pcas)

        if 'train' in config['tasks'] and config['tasks']['train'] and not config['use_cache']['train']:
            save_file(path.join(directory, 'models.pkl'), models)

        if 'train' in config['use_cache'] and config['use_cache']['train']:
            models = load_file(path.join(directory, 'models.pkl'))

        for fold_id, scene, _, testing in dataset.folds:
            testing_data_file = '%s-%s-testing_data.pkl' % (scene, fold_id)
            system.models = models[scene][fold_id]
            system.normalizer = normalizers[scene][fold_id]
            system.pca = pcas[scene][fold_id]

            testing_data_file_full = path.join(features_directory, testing_data_file)

            if config['tasks']['extract_features']:
                system.add_testing(testing)
                save_file(testing_data_file_full, system.testing_data)

            if config['use_cache']['extract_features']:
                system.testing_data = load_file(testing_data_file_full)
            if not os.path.exists(path.join('results', config['experiment_name'], 'folds')):
                os.makedirs(path.join('results', config['experiment_name'], 'folds'))
            if config['tasks']['classify']:
                print('Classifying')
                if threshold:
                    for i in range(-300, 301, 5):
                        print(i)
                        guessed_labels = system.classify(i)
                        # print(guessed_labels)
                        filename = '%s_fold%i_results.txt' % (scene, fold_id)
                        dataset.store_results(filename, guessed_labels, i)
                else:
                    guessed_labels = system.classify(160)
                    print(guessed_labels)
                    filename = '%s_fold%i_results.txt' % (scene, fold_id)
                    dataset.store_results(filename, guessed_labels, 160)
            system.reset()
    else:
        for scene, training_data in dataset.training:
            print('CHALLENGE MODE')
            system.add_training(training_data)
            system.create_normalizer()
            system.train()
            for i in range(-300, 300):
                os.mkdir(path.join('results', config['experiment_name'], 'folds', i))
                dataset.store_results('folds/'+str(i)+'/'+output_file + '_' + filename, guessed_labels)
                guessed_labels = system.classify(dataset.evaluation(scene))
                filename = 'results_evaluate_%s.txt' % (scene)
            system.reset()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Config file for an experiment')
    parser.add_argument('--mode', help='Mode to run the system in (classify, threshold, train, extract_features)')
    parser.add_argument('--cache', help='Directory for caching files')
    parser.add_argument('--results', help='Directory for results files')
    parser.add_argument('--seed', help='Seed for the randomness')
    parser.add_argument('--setup', help='location of evaluation setup')
    args = parser.parse_args()
    main(args)
