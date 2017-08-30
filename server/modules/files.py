from os import path, makedirs
from werkzeug.datastructures import FileStorage

def require_file_path(func):
    def wrapper(self, *args):
        if self.file_path is None:
            raise ValueError('File path is required.')
        return func(self, *args)
    return wrapper

class File:
    
    def __init__(self, file_or_path):
        if self.is_file_like(file_or_path):
            self.file = file_or_path
            self.file_path = None
        elif isinstance(file_or_path, str):
            self.file = self._open(file_or_path)
            self.file_path = file_or_path
        else:
            raise ValueError('Invalid file type')
    
    @property
    def extension(self):
        return self.filename.split('.')[-1].lower()
    
    @property
    @require_file_path
    def filename(self):
        return path.basename(self.file_path)
    
    @property
    @require_file_path
    def directory(self):
        return path.dirname(self.file_path)
    
    def is_file_like(self, obj):
        return hasattr(obj, 'save')
    
    @require_file_path
    def save(self):
        makedirs(self.directory)
        self.file.save(self.file_path)
    
    def close(self):
        self.file.close()


class AudioFile(File):

    def _open(self, path):
        return FileStorage(open(path, 'rb'))
    
class LabelFile(File):

    def save(self):
        pass