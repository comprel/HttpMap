from lib.ip import getRequestIpaddress
from lib.format_json import to_str
from core.controller import BaseResponse
from driver.CACHE.Redis import Redis
from dbs.host.api import HostApi
from dbs.host.api import IpaddressApi
from dbs.host.graphApi import HostGraphApi


class HostRegister(BaseResponse):
    allowed_methods = ["POST"]

    def on_graph_create(self, uuid, data):
        graphData = {"uuid": uuid,
                     "hostname": data.get("hostname"),
                     "ipaddress": data.get("ipaddress")}
        return HostGraphApi().insert(graphData)

    def on_ipaddress_create(self, uuid, data):
        ipaddress_data = {"ip": data.get("ipaddress"), "host_id": uuid}
        return IpaddressApi().insert(ipaddress_data)

    def create(self, req, data, resp, **kwargs):
        if not data.get("id"):
            raise ValueError("主机注册缺少UUID")
        hostApi = HostApi()
        uuid = data["id"]
        hostRegisterData = hostApi.get(primiry_id=uuid)
        if hostRegisterData:
            raise ValueError("UUID:%s 已注册， 注册信息 - HOSTNAME %s - IP: " %
                             (uuid, hostRegisterData["hostname"]), hostRegisterData["ipaddress"])

        # 一台主机可能拥有多个ip， 注册主机以请求IP进行注册（默认情况下， 该ip应该为默认出口ip）
        data["ipaddress"] = getRequestIpaddress(req)
        self.on_ipaddress_create(uuid, data)
        self.on_graph_create(uuid, data)
        count, cid = hostApi.insert(data)
        Redis.set(uuid, to_str(data=data))
        return count.cid


class HostUnRegister(BaseResponse):
    allowed_methods = ["DELETE"]

    def on_graph_delete(self, uuid):
        return HostGraphApi().delete(uuid)

    def on_ipaddress_delete(self, uuid):
        return IpaddressApi().delete_many(filter={"host_id": uuid})

    def delete(self, req, data, resp, **kwargs):
        uuid = kwargs.pop("uuid", None)
        _host = HostApi().get(primiry_id=uuid)
        if not _host:
            return {}
        Redis.delete(uuid)
        self.on_ipaddress_delete(uuid)
        self.on_graph_delete(uuid)
        return HostApi().delete(primiry_id=uuid)
