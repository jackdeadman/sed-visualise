from os import path, makedirs, getcwd, remove, rmdir

class Logger:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, logging_level):
        self.logging_level = logging_level

    def log(self, msg):
        if self.logging_level > 1:
            print(msg)

    def log_success(self, msg):
        self.log(self.OKGREEN + msg + self.ENDC)

    def log_fail(self, msg):
        self.log(self.FAIL + msg + self.ENDC)

class Generator:

    def __init__(self, name, base_path):
        self.name = name
        self._base_path = base_path
        self.__logger = Logger(3)

    # === Useful paths ===

    @property
    def system_path(self):
        if self._base_path is None:
            msg = 'self._base_path has not been defined'
            raise NotImplementedError(msg)
        return path.join(self._base_path, self.name)

    @property
    def templates_path(self):
        current_path = path.dirname(__file__)
        return path.join(current_path, 'templates')


    # === Useful Helpers ===

    def ensure_dir(self, directory):
        if not path.exists(directory):
            makedirs(directory)

    def remove_dir(self, directory):
        if path.exists(directory):
            rmdir(directory)

    def generate(self):
        msg = 'Need to provide a generate method when overriding'
        raise NotImplementedError(msg)

    @property
    def output_file(self):
        return path.join(self.system_path, self.filename)

    def remove(self):
        if path.isfile(self.output_file):
            remove(self.output_file)
            self.log_remove()

    def log_remove(self, file_=None):
        if file_ is None:
            file_ = self.output_file
        msg = 'Successfully removed %s' % file_
        self.__logger.log_fail(msg)

    def log_save(self, file_=None):
        if file_ is None:
            file_ = self.output_file
        msg = 'Successfully created %s' % file_
        self.__logger.log_success(msg)
