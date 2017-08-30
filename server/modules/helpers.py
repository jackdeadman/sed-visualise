from flask import flash, url_for, send_file
from io import BytesIO
from os import path, makedirs

def redirect_with_message(url, message):
    flash(message)
    return url_for(url)

def ensure_dir(file_path):
    directory = path.dirname(file_path)
    if not path.exists(directory):
        makedirs(directory)

def send_wav(path_to_file):
    return send_file(
         path_to_file, 
         mimetype="audio/wav", 
         as_attachment=False, 
         attachment_filename=path.basename(path_to_file))

def send_text(text, filename=None):
    file = BytesIO()
    file.write(str.encode(text))
    file.seek(0)

    return send_file(
        file,
        mimetype="text/plain", 
        as_attachment=False, 
        attachment_filename=filename)
