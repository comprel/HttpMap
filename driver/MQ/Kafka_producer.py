# coding:utf-8

import traceback
from kafka import KafkaProducer
from core.conf import MQ_SERVICE
from core.conf import MQ_KAFKA_TOPIC
from lib.logs import logger
from lib.uuidlib import allocate_uuid
from lib.format_json import to_str
from driver.MQ.base import MQBase

producer = KafkaProducer(bootstrap_servers=MQ_SERVICE)


class KafkaProducerClient(MQBase):
    def __init__(self):
        self.client = None

    def __del__(self):
        self.client = None

    def connector(self):
        if self.client is None:
            self.client = producer

    def __format_msg(self, msg):
        if isinstance(msg, (dict, list)):
            msg = to_str(msg)
        return msg

    def send(self, msg, key=None, partition=None, timestamp_ms=None):
        _id = allocate_uuid()
        msg = {"_id": _id, "data": msg}
        msg = self.__format_msg(msg)
        self.connector()
        try:
            self.client.send(MQ_KAFKA_TOPIC, value=msg, key=key, partition=partition, timestamp_ms=timestamp_ms)
            logger.debug("SEND _ID: %s" % _id)
            return _id
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(e.args)
            raise e
