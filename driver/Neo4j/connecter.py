# coding:utf-8

from py2neo import Graph
from retrying import retry
from core.conf import NEO4J_SERVICE
from core.conf import NEO4J_HTTP_PORT
from core.conf import NEO4J_BOLT_PORT
from core.conf import NEO4J_USERNAME
from core.conf import NEO4J_PASSWORD

graph = Graph(NEO4J_SERVICE,
              http_port=NEO4J_HTTP_PORT,
              bolt_port=NEO4J_BOLT_PORT,
              username=NEO4J_USERNAME,
              password=NEO4J_PASSWORD)


@retry(stop_max_attempt_number=10, wait_fixed=3)
def get_connection():
    return graph
