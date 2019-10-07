# coding:utf-8

from lib.uuidlib import allocate_uuid
from driver.Neo4j.Neo4j import Neo4jDriver


class HostGraphApi(Neo4jDriver):
    table_name = "host"
    primary_key = "uuid"
