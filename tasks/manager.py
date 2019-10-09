import traceback
from lib.logs import logger
from lib.format_json import to_str
from driver.MQ.kafka_consumer import KafkaConsumerClient
from dbs.access.mongoApi import AccessMongoApi
from dbs.host.api import IpaddressApi
from dbs.host.graphApi import HostGraphApi


class AccessDraw(KafkaConsumerClient):
    mongoClient = AccessMongoApi()

    def __init__(self):
        super(AccessDraw).__init__()

    def __create_cloud_node(self):
        uuid = "netmapcloud"
        _graph_data = HostGraphApi().queryone(primary_key=uuid)
        if not _graph_data:
            HostGraphApi().insert(data={"uuid": uuid, "ipaddress": "0.0.0.0",
                                        "hostname": "__netmapcloud__", "describe": "互联网访问"})

    def callback(self, msg):
        '''
        :param msg:
        :return:
        '''
        # TODO  识别访问src ip是否为外网地址， 若为外网地址， 则统一归属为netmapcloud
        try:
            access_data = {"uuid": msg.get("id"), "src": msg.get("src"),
                           "dest": msg.get("dest"), "port": msg.get("port")}
            self.mongoClient.insert(access_data)
            ip_data = IpaddressApi().get(primiry_id=msg.get("src"))
            if ip_data:
                HostGraphApi().create_relation(primary_key1=msg.get("id"),
                                               primary_key2=ip_data.get("host_id"),
                                               re_type="access", port=msg.get("port"),
                                               access="%s_%s" % (msg.get("src"), msg.get("dest")))
        except:
            logger.info(traceback.format_exc())
            logger.info("Access Drawer failed: %s" % to_str(msg))
