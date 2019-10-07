# coding:utf-8

import redis
from core.conf import CACHE_SERVICE
from core.conf import CACHE_PORT
from core.conf import CACHE_DB
from core.conf import CACHE_PASSWORD
from core.conf import CACHE_MAX_CONNECTION
from driver.CACHE.base import CacheBase

pool = redis.ConnectionPool(host=CACHE_SERVICE, port=CACHE_PORT, password=CACHE_PASSWORD,
                            db=CACHE_DB, max_connections=CACHE_MAX_CONNECTION)
redis_connector = redis.Redis(connection_pool=pool, socket_timeout=2)


class Redis(CacheBase):
    @classmethod
    def connector(cls):
        return redis_connector

    @classmethod
    def get(cls, key):
        try:
            conn = cls.connector()
            res = conn.get(key)
            conn = None
            return res
        except:
            return None

    @classmethod
    def set(cls, key, value, timeout=None):
        try:
            conn = cls.connector()
            conn.set(name=key, value=value)
            if timeout:
                conn.expire(name=key, time=timeout)
            conn = None
            return True
        except:
            return False

    @classmethod
    def delete(cls, key):
        try:
            conn = cls.connector()
            conn.delete(key)
            conn = None
            return True
        except:
            return False

    @classmethod
    def incr(cls, key, value):
        try:
            conn = cls.connector()
            conn.incr(name=key, amount=value)
            conn = None
            return True
        except:
            return False

    @classmethod
    def decr(cls, key, value):
        try:
            conn = cls.connector()
            conn.decr(name=key, amount=value)
            conn = None
            return True
        except:
            return False
