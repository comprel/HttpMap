# coding:utf-8

import json
import time
import traceback
from kafka import KafkaConsumer
from lib.logs import logger
from core.conf import MQ_SERVICE
from core.conf import MQ_KAFKA_TOPIC
from driver.MQ.base import MQBase

consumer = KafkaConsumer(bootstrap_servers=MQ_SERVICE)
consumer.subscribe(topics=MQ_KAFKA_TOPIC)


class KafkaConsumerClient(MQBase):
    def __init__(self):
        self.client = None

    def __del__(self):
        self.client = None

    def connector(self):
        if self.client is None:
            self.client = consumer

    def callback(self, msg):
        '''
        消息处理实现该方法
        :param msg:
        :return:
        '''
        raise AttributeError("not define msg callback")

    def on_message(self, message):
        for msg in message:
            logger.debug("TOPIC: %s - PARTION: %s -KEY:%s" % (msg.topic, msg.partion, msg.key))
            data = json.loads(msg.value)
            logger.debug("POLL _ID: %s" % data.get("_id"))
            try:
                self.callback(data.get("data"))
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.error(e.args)
                raise e

    def run(self):
        '''
        服务启动函数， 一次获取最多100条记录，进行处理
        若无消息， 则延迟1s进行获取
        若需要防止重复消息，需callback执行实现幂等性
        :return:
        '''
        self.connector()
        while True:
            msg = self.client.poll(timeout_ms=5, max_records=100)
            if msg:
                self.on_message(msg)
            else:
                time.sleep(1)
