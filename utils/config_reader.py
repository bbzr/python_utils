import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = '/'.join(current_dir.split('/')[:-1])


class SingletonMeta(type):
    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Config(metaclass=SingletonMeta):
    def __init__(self):
        with open(project_root_dir + '/config.yml', 'r') as f:
            self.data = load(f.read(), Loader=Loader)
        

def get_config():
    conf = Config()
    return conf.data
