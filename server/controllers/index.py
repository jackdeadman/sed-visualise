from flask import Blueprint, render_template, redirect

from modules.config import messages
from modules.helpers import redirect_with_message
from modules.uploaders import AudioUploader

from decorators.uploaders import file_uploader

index = Blueprint('index', __name__)

@index.route('/')
def root():
    return render_template('index.html')

@index.route('/upload', methods=['POST'])
@file_uploader
def upload_audio(file_):
  uploader = AudioUploader(file_)
  try:
    saved_audio_file = uploader.save()
  except Exception as e:
    print(e)
    msg = messages['upload_failed']
    return redirect_with_message('index.root', msg)
  
  return redirect('/play/' + uploader.code)

