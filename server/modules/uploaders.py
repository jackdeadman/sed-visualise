from os import path, makedirs
from random import randint

from hashids import Hashids

from modules.config import app_config

hashids = Hashids(salt='1234')

class UploaderException(Exception):
  pass

class InvalidFileException(UploaderException):
  pass

class Uploader:

  def __init__(self, file_):
    self.allowed_extensions = []
    self.file = file_
  
  @property
  def extension(self):
    return self.filename.split('.')[-1].lower()

  @property
  def filename(self):
    return self.file.filename

  @property
  def allowed_file(self):
    return self.extension in self.allowed_extensions
  
  @property
  def __class_name(self):
    return self.__class_name.__name__

  def save(self):
    msg = 'Cannot save %s' % self.__class_name
    raise NotImplementedError(msg)

class AudioUploader(Uploader):
  def __init__(self, file_):
    super().__init__(AudioFile(file_))
    self.allowed_extensions = ['wav']
    self.__code = None
  
  def save(self, location=None):
    if not self.allowed_file:
      raise InvalidFileException('Please upload a wav file.')

    if location is None:
      location = app_config['upload_folder']

    code = hashids.encode(randint(0, 10000))
    file_path = path.join(location, code, 'audio.wav')

    self.file.file_path = file_path
    self.file.save()
    self.__code = code
  
  @property
  def code(self):
    if self.__code is None:
      raise ValueError('No code for audio file.')
    
    return self.__code
  
  @property
  def file_path(self):
    return self.file_.file_path
  
  @file_path.setter
  def file_path(self, path):
    self.file.file_path = path
