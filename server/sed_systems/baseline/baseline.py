# Library
from modules.classifier import Classifier

'''
PLEASE NOTE: You will need to restart the server after making changes
to this file.
'''

class Baseline(Classifier):

    @property
    def use_caching(self):
        return False

    @property
    def config(self):
        return {
            'id': 'baseline', # filename
            'title': '[TITLE TO APPEAR ON THE FRONTEND]',
            'description': '[DESCRIPTION TO APPEAR ON THE EFRONTEND]'
        }

    def setup(self):
        """
        Setup the classifier e.g load models.
        This is called only once on the server startup,
        unless use_caching=False.
        """
        pass

    def classify(self, audio):
        """
        Run the classifer using the loaded models.
        @param audio: Audio object of the file being classified
        @return numpy array, location to text file or text file object
        """
        return '\n'.join([
            '0\t10\tObject Impact',
            '0\t20\tObject Impact1',
            '30\t35\tObject Impact2'
        ])
