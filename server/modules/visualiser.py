from os import path

from modules.config import app_config
from modules.files import AudioFile

class Visualiser:

    def __init__(self, code, location=None):
        self.__code = code

        if location is None:
            location = app_config['upload_folder']
        
        audio_file = path.join(location, code, 'audio.wav')
        self.audio = AudioFile(audio_file)

    @property
    def code_location(self):
        return self.audio.directory

    @property
    def code(self):
        return self.__code

    @property
    def is_valid(self):
        return path.isdir(self.code_location)
    
    @property
    def audio_file(self):
        return self.audio.file_path
    
    def generate_labels(self):
        if self.classifier is None:
            raise ValueError('No classifier found.')
        
        return self.classifier.classify_internal(self.audio)