# coding:utf-8

from datetime import datetime
from lib.uuidlib import allocate_uuid
from lib.format_json import to_str, to_json
from core.common_exception import ResourceNotFound
from driver.databases.mysql import Mysql
from driver.CACHE.Redis import Redis
from dbs.host.model import HostTable
from dbs.host.model import IpaddressTable


class HostApi(Mysql):
    DBModel = HostTable
    primary_key = "id"

    def _before_insert(self, data):
        if not data[self.primary_key]:
            raise ValueError("host uuid not permit null")
        return data

    def _before_update(self, data):
        data["updated_time"] = datetime.now()
        return data

    def valitdae_host(self, uuid):
        cache_data = Redis.get(uuid)
        if cache_data:
            if cache_data == "-":
                raise ResourceNotFound("主机记录不存在")
            return to_json(cache_data)

        _host = self.get(primiry_id=uuid)
        if not _host:
            Redis.set(uuid, "-")
            raise ResourceNotFound("主机记录不存在")
        Redis.set(uuid, to_str(_host))
        return _host


class IpaddressApi(Mysql):
    DBModel = IpaddressTable
    primary_key = "ip"

    def _before_insert(self, data):
        if not data[self.primary_key]:
            raise ValueError("ip not permit null")
        return data

    def _before_update(self, data):
        data["updated_time"] = datetime.now()
        return data
