from os import path
import yaml
from shutil import copy2

from .generator import Generator

class ConfigGenerator(Generator):
    """
    Abstract Base Config generator
    """
    def __init__(self, name, base_path):
        super().__init__(name, base_path)
        self.defaults = {
            'name': name,
            'description': 'No description provided.',
            'configurations': [
                'default'
            ]
        }

class ConfigGeneratorYaml(ConfigGenerator):

    def __init__(self, name, base_path):
        super().__init__(name, base_path)
        self.filename = 'config.yaml'

    def generate(self):
        output_name = path.join(self.system_path, self.filename)
        with open(output_name, 'w') as output_file:
            yaml.dump(self.defaults, output_file)

        self.log_save(output_name)


class ClassifierGenerator(Generator):

    def __init__(self, name, base_path):
        super().__init__(name, base_path)
        self.filename = 'classifier.py'

    @property
    def classifier_template(self):
        return path.join(self.templates_path, self.filename)

    def generate(self):
        output_file = path.join(self.system_path, self.filename)
        copy2(self.classifier_template, output_file)
        self.log_save(output_file)

class SystemGenerator(Generator):

    def __init__(self, name, generators=None):
        super().__init__(name, 'systems')
        self.generators = generators

        if generators is None:
            # Default generators
            self.generators = [
                ConfigGeneratorYaml(name, self._base_path),
                ClassifierGenerator(name, self._base_path)
            ]

    @property
    def system_path(self):
        return path.join(self._base_path, self.name)

    def generate(self):
        # Create the directory
        super().ensure_dir(self.system_path)

        for generator in self.generators:
            generator.generate()
