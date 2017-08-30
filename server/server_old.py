from flask import Flask, request, redirect, url_for, jsonify, flash, render_template, send_file
from werkzeug.utils import secure_filename

import json
import yaml
from hashids import Hashids
import os
import random
import pickle
from io import BytesIO

from ClassifierFactory import create_classifier

hashids = Hashids(salt='1234')

with open('server/config.yaml', 'r') as f:
    config = yaml.load(f)

app = Flask(__name__, static_url_path='', static_folder='../static')
app.config['UPLOAD_FOLDER'] = config['upload_folder']
app.secret_key = 'rjPBtXTp7r^X)g6vco69B7,IH^5i)5'

ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_audio():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash(messages.INVALID_AUDIO_FILE)
            return redirect(url_for('root'))
        file = request.files['file']

        if file.filename == '':
            flash('Error: You need to choose a file to upload.')
            return redirect(url_for('root'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            code = hashids.encode(random.randint(0, 10000))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], code)
            os.mkdir(file_path)

            file.save(os.path.join(file_path, 'audio.wav'))
            return redirect('/play/'+code)
            return jsonify({
                'code': code
            })
        else:
            flash('Error: Please upload a .wav file.')
            return redirect(url_for('root'))

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/play/<id>')
def play(id):
    cwd = os.getcwd()
    audio_file = os.path.join(cwd, 'static', 'audio', id, 'audio.wav')
    if os.path.isfile(audio_file):
        return render_template('index.html')
    else:
        flash('Cannot find the audio file.')
        return redirect(url_for('root'))

@app.route('/classify/<classifier_id>/<audio_id>')
def classify(classifier_id, audio_id):

    classifier = get_classifier(classifier_id)
    classifier.setup()

    audio_file = get_audiofile(audio_id)
    labels = classifier.classify(audio_file)
    return send_file(labels, as_attachment=False, mimetype='text/plain')


def train(id):
    system = create_classifier(
        features=request.args.getlist('features[]'),
        scene=request.args.get('scene'),
        norm_path=request.args.get('norm_path'),
        model_path=request.args.get('model_path')
    )

    if request.args.get('threshold'):
        threshold = int(request.args.get('threshold'))
    else:
        threshold = 160

    cwd = os.getcwd()
    audio_file = os.path.join(cwd, 'static', 'audio', id, 'audio.wav')
    system.add_testing([audio_file])
    guessed_labels = system.classify(threshold)

    strIO = BytesIO()
    for file in guessed_labels.values():
        for line in file:
            line = map(str, line)
            to_write = '\t'.join(line)+'\n'
            print(str.encode(to_write))
            strIO.write(str.encode(to_write))
    strIO.seek(0)
    return send_file(strIO, as_attachment=False, mimetype='text/plain')

if __name__ == '__main__':
    app.run(threaded=True)
