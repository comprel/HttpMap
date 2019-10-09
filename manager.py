# coding: utf-8

from wsgiref import simple_server
from lib.logs import logger
from core.conf import PORT
from core.conf import IPPADDRESS
from core.base import APP

if __name__ == '__main__':
    print("Starting ...")
    httpd = simple_server.make_server(IPPADDRESS, PORT, APP)
    logger.info("service listen at %s:%s" % (IPPADDRESS, PORT))
    httpd.serve_forever()
