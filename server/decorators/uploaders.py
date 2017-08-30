from flask import request, url_for

from modules.config import messages
from modules.helpers import redirect_with_message

def file_uploader(func):
    def wrapper(*args):
        root_url = url_for('index.root')

        if 'file' not in request.files:
            msg = messages['no_file_uploaded']
            return redirect_with_message(root_url, msg)
        
        file_ = request.files['file']
        return func(file_, *args)
    
    return wrapper