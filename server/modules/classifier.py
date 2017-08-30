from os import listdir, path
import importlib

from modules.config import app_config

class ClassifierFactory:
    
    def __init__(self, location=None):
        if location is None:
            location = app_config['systems_folder']
        self.location = location

    
    def get(self, classifier_name):
        module_name = self.__module_name(classifier_name)
        module = importlib.import_module(module_name)
        klass = getattr(module, classifier_name.capitalize())
        return klass()

    def __module_name(self, classifier_name):
        return '.'.join([self.location, classifier_name, classifier_name])
    
    @property
    def all(self):
        return map(self.get, listdir(self.location))
    
    @property
    def all_configs(self):
        return list(map(lambda c: c.config, self.all))

class ClassifierPool:
    def __init__(self, factory):
        self.pool = {}
        self.classifier_factory = factory
    
    def get(self, classifier_name):
        if classifier_name in self.pool:
            return self.pool[classifier_name]
        classifier = self.classifier_factory.get(classifier_name)
        self.pool[classifier_name] = classifier
        return classifier

class Classifier:

    def __init__(self):
        self.__setup = False
    
    @property
    def config(self):
        return {}
    
    @property
    def use_caching(self):
        return True
    
    def has_labels_for(self, audio):
        return False
    
    def classify_internal(self, audio):
        if self.use_caching:
            if not self.__setup:
                self.setup()
                self.__setup = True

            if self.has_labels_for(audio):
                return audio.labels_for(self)
        
        return self.classify(audio)
    
    # User methods to override
    def setup(self):
        pass
    
    def classify(self):
        return []