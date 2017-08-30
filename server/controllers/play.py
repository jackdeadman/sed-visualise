import json

from flask import Blueprint, render_template

from modules.classifier import ClassifierPool, ClassifierFactory
from modules.helpers import redirect_with_message, send_wav, send_text
from modules.serialisers import TextLabelSerialiser
from modules.visualiser import Visualiser

play = Blueprint('play', __name__)
classifier_factory = ClassifierFactory()
classifier_pool = ClassifierPool(classifier_factory)

@play.route('/play/<code>')
def root(code):
    vis = Visualiser(code)
    if vis.is_valid:
        return render_template('index.html')
    msg = 'Error: Not a valid code'
    return redirect_with_message(msg)

@play.route('/audio/<audio_code>/audio.wav')
def audio(audio_code):
    vis = Visualiser(audio_code)
    try:
        return send_wav(vis.audio_file)
    except Exception as e:
        print(e)
        raise e

@play.route('/classify/<classifier_code>/<audio_code>')
def classify(classifier_code, audio_code):
    vis = Visualiser(audio_code)
    vis.classifier = classifier_pool.get(classifier_code)
    serialiser = TextLabelSerialiser()

    try:
        labels_matrix = vis.generate_labels()
        labels = serialiser.serialise(labels_matrix)
    except Exception as e:
        print(e)
        raise e
    return send_text(labels, 'labels.txt')

import time

@play.route('/classifiers/')
def classifiers():
    time.sleep(1)
    configs = classifier_factory.all_configs
    return json.dumps({ 'classifiers': configs })