# coding:utf-8

class CacheBase(object):
    @classmethod
    def incr(cls, key, value):
        raise AttributeError("not define")

    @classmethod
    def decr(cls, key, value):
        raise AttributeError("not define")

    @classmethod
    def set(cls, key, value, timeout=None):
        raise AttributeError("not define")

    @classmethod
    def delete(cls, key):
        raise AttributeError("not define")

    @classmethod
    def get(cls, key):
        raise AttributeError("not define")

    @classmethod
    def get_int(cls):
        raise AttributeError("not define")
