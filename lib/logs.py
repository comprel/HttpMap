# coding=utf8

import threading
import logging
import logging.config
import logging.handlers
from core.conf import LOG_NAME
from core.conf import LOG_LEVEL
from core.conf import LOG_MAX_SIZE
from core.conf import LOG_BACKUP

levelmap = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def singleton(cls):
    """单例模式装饰器"""
    instances = {}
    lock = threading.Lock()

    def _singleton(*args, **kwargs):
        with lock:
            fullkey = str((cls.__name__, tuple(args), tuple(kwargs.items())))
            if fullkey not in instances:
                instances[fullkey] = cls(*args, **kwargs)
        return instances[fullkey]

    return _singleton


@singleton
def logsetup():
    filename = LOG_NAME
    handler = logging.handlers.RotatingFileHandler(filename=filename, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP)
    logging.getLogger(filename).setLevel(levelmap.get(LOG_LEVEL, logging.INFO))
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger(filename).addHandler(handler)


def get_logger():
    logsetup()
    return logging.getLogger(LOG_NAME)


logger = get_logger()
