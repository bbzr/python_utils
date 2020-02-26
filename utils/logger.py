import logging
from logging.handlers import RotatingFileHandler
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = '/'.join(current_dir.split('/')[:-1])


class SingletonMeta(type):
    _instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)
        return self._instance


class Logger(metaclass=SingletonMeta):
    def __init__(self, name, path, log_level=logging.DEBUG):
        self.file_size_bytes = 10485760
        self.files_count = 10
        self.name = name
        self.filepath = os.path.normpath(path + '/' + self.name + '.log')
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('[%(asctime)s.%(msecs)03f][%(name)s][%(levelname)s] %(message)s', "%Y-%m-%dT%H:%M:%S")
        logfile_handler = RotatingFileHandler(self.filepath, maxBytes=self.file_size_bytes, backupCount=self.files_count)
        stdout_handler = logging.StreamHandler(sys.stdout)
        logfile_handler.setFormatter(formatter)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(logfile_handler)
        self.logger.addHandler(stdout_handler)

    def debug(self, msg):
        self._log(logging.DEBUG, msg, 'DEBUG')

    def info(self, msg):
        self._log(logging.INFO, msg, 'INFO')

    def warning(self, msg):
        self._log(logging.WARNING, msg, 'WARNING')

    def error(self, msg):
        self._log(logging.ERROR, msg, 'ERROR')

    def critical(self, msg):
        self._log(logging.CRITICAL, msg, 'CRITICAL')

    def _log(self, level, msg, lvl_name):
        self.logger.log(level, str(msg))


def get_logger():
    return Logger(name='script', path=project_root_dir + '/logs', log_level=logging.INFO)
