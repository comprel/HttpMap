# coding:utf-8


class MQBase(object):
    def producer(self, msg, topic):
        raise AttributeError("not define")

    def consumer(self, msg, topic):
        raise AttributeError("not define")
