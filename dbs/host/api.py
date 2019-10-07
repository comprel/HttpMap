# coding:utf-8

from lib.uuidlib import allocate_uuid
from driver.databases.mysql import Mysql
from dbs.host.model import HostTable
from dbs.host.model import IpaddressTable


class HostApi(Mysql):
    DBModel = HostTable
    primary_key = "id"

    def _before_insert(self, data):
        if not data[self.primary_key]:
            raise ValueError("host uuid not permit null")
        return data

    def valitdae_host(self, uuid):
        _host = self.get(primiry_id=uuid)
        if not _host:
            raise ValueError("主机记录不存在")
        return _host


class IpaddressApi(Mysql):
    DBModel = IpaddressTable
    primary_key = "ip"

    def _before_insert(self, data):
        if not data[self.primary_key]:
            raise ValueError("ip not permit null")
        return data
