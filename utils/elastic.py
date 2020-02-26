from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
import ssl
from utils.config_reader import get_config


class SingletonMeta(type):
    _instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)
        return self._instance


class Elastic(Elasticsearch, metaclass=SingletonMeta):
    pass


def get_es_instance():
    conf = get_config()
    ssl_context = create_ssl_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    user = conf['es']['user']
    password = conf['es']['password']
    if user and password:
        auth = (user, password)
    else:
        auth = None

    return Elastic(
        hosts=[conf['es']['host']],
        http_auth=auth,
        scheme=conf['es']['scheme'],
        port=conf['es']['port'],
        ssl_context=ssl_context
    )

