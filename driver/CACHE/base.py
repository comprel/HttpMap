# coding:utf-8

class CacheBase(object):
    def incr(self, key, value):
        raise IndentationError("not define")

    def decr(self, key, value):
        raise IndentationError("not define")

    def set(self, key, value, timeout=None):
        raise IndentationError("not define")

    def get(self, key):
        raise IndentationError("not define")

    def get_int(self):
        raise IndentationError("not define")
