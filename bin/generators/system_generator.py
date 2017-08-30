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
            'configurations': {
                'default': {
                    'name': 'Default configuration',
                    'description': 'No description provided.'
                }
            }
        }

class ConfigGeneratorYaml(ConfigGenerator):

    def __init__(self, name, base_path):
        super().__init__(name, base_path)
        self.filename = 'config.yaml'

    def generate(self):
        with open(self.output_file, 'w') as output_file:
            yaml.dump(self.defaults, output_file, default_flow_style=False)


class ClassifierGenerator(Generator):

    def __init__(self, name, base_path):
        super().__init__(name, base_path)
        self.filename = 'default.py'

    @property
    def classifier_template(self):
        return path.join(self.templates_path, 'classifier.py')

    def generate(self):
        output_file = path.join(self.system_path, self.filename)
        copy2(self.classifier_template, self.output_file)

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
            # Only create new files
            if not path.isfile(generator.output_file):
                generator.generate()
                generator.log_save()

    def remove(self):
        # Clean removal
        for generator in self.generators:
            generator.remove()

        try:
            super().remove_dir(self.system_path)
            self.log_remove(self.system_path)
        except OSError:
            # Directory may not be empty, this will throw an OSError.
            # Maybe add a prompt to the user asking them to continue anyway?
            pass
