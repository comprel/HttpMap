from lib.format_json import to_str
from core.controller import BaseResponse
from driver.CACHE.Redis import Redis
from dbs.host.api import HostApi
from dbs.host.api import IpaddressApi
from dbs.host.graphApi import HostGraphApi


class HostHandler(BaseResponse):
    allowed_methods = ["GET"]

    def list(self, req, data, resp, **kwargs):
        return HostApi().query(filter=data, **kwargs)


class HostIdHandler(BaseResponse):
    allowed_methods = ["GET", "PATCH", "DELETE"]

    def detail(self, req, data, resp, **kwargs):
        uuid = kwargs.pop("uuid", None)
        return HostApi().get(primiry_id=uuid)

    def on_graph_update(self, uuid, data):
        graph_update = {}
        if "ipaddress" in data.keys():
            graph_update["ipaddress"] = data["ipaddress"]
        if "hostname" in data.keys():
            graph_update["hostname"] = data['hostname']
        HostGraphApi().update(uuid, data=graph_update)

    def update(self, req, data, resp, **kwargs):
        uuid = kwargs.pop("uuid", None)
        if "ipaddress" in data.keys():
            raise ValueError("ipaddress 不允许更新， 默认为主机注册ip， 如需更改请重新注册")
        count, after_data = HostApi().update(primiry_id=uuid, data=data)
        if count:
            Redis.delete(uuid)
            self.on_graph_update(uuid=uuid, data=data)
        return count, after_data

    def on_graph_delete(self, uuid):
        return HostGraphApi().delete(primary_key=uuid)

    def on_ipaddress_delete(self, uuid):
        return IpaddressApi().delete_many(filter={"host_id": uuid})

    def delete(self, req, data, resp, **kwargs):
        uuid = kwargs.pop("uuid", None)
        result = HostApi().delete(primiry_id=uuid)
        if result:
            Redis.delete(uuid)
            self.on_graph_delete(uuid)
            self.on_ipaddress_delete(uuid)
        return result
