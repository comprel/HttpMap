# coding : utf-8

from lib.ConfigReader import ConfigReader

Config = ConfigReader()

CACHE_FLUSH_TIME = Config.getInt("DEFAULT", "cache_flush_time", default=7200)
IPPADDRESS = Config.get("DEFAULT", "ipaddress", default="0.0.0.0")
PORT = Config.getInt("DEFAULT", "port", default=8080)

loadsModel = Config.get("CONTROLLER", "load.controller", default="all")
if loadsModel != "all":
    loadsModel.split(",")

LOG_NAME = Config.get("LOG", "path", default="./logs/service.log")
LOG_LEVEL = Config.get("LOG", "level", default="INFO")
LOG_MAX_SIZE = Config.getInt("LOG", "max_size", default="200") * 1024 * 1024
LOG_BACKUP = Config.getInt("LOG", "backup_count", default=3)
LOG_MSG_MAX_LEN = Config.getInt("LOG", "msg.max.len", default=2048)

MQ_TYPE = Config.get("MQ", "type", default="kafka")
MQ_SERVICE = Config.getList("MQ", "service")
MQ_KAFKA_TOPIC = Config.getList("MQ", "kafka.topic")
MQ_KAFKA_GROUP = Config.get("MQ", "kafka.group", "NetmapGroup")
MQ_DRIVERS = Config.get("MQ", "drivers", default="")

CACHE_TYPE = Config.get("CACHE", "type", default="redis")
CACHE_SERVICE = Config.getList("CACHE", "service")
CACHE_PORT = Config.getInt("CACHE", "port", default=6379)
CACHE_DB = Config.getList("CACHE", "db", default=0)
CACHE_PASSWORD = Config.getList("CACHE", "password")
CACHE_MAX_CONNECTION = Config.getInt("CACHE", "max.connection", default=3000)
CACHE_DRIVERS = Config.get("CACHE", "drivers", default="")

NEO4J_SERVICE = Config.get("NEO4J", "service")
NEO4J_HTTP_PORT = Config.getInt("NEO4J", "http_port", 7474)
NEO4J_BOLT_PORT = Config.get("NEO4J", "bolt_port", 7687)
NEO4J_USERNAME = Config.get("NEO4J", "username", None)
NEO4J_PASSWORD = Config.get("NEO4J", "password", None)

MYSQL_SERVICE = Config.get("MYSQL", "service")

MONGO_SERVICE = Config.get("MONGODB", "service")
MONGO_PORT = Config.getInt("MONGODB", "port", default=27017)
MONGO_DB = Config.get("MONGODB", "db", default="netmap")
MONGO_USER = Config.get("MONGODB", "user")
MONGO_PASSWORD = Config.get("MONGODB", "password")