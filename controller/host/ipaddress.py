from lib.ip import is_ip
from core.controller import BaseResponse
from dbs.host.api import HostApi
from dbs.host.api import IpaddressApi


class IpAddressHandler(BaseResponse):
    '''
    主机ip 对用户不提供创建数据功能， 创建由上报数据进行
    '''
    allowed_methods = ["GET"]

    def list(self, req, data, resp, **kwargs):
        return IpaddressApi().query(filter=data, **kwargs)


class IpAddressIdHandler(BaseResponse):
    allowed_methods = ["GET", "PATCH", "DELETE"]

    def detail(self, req, data, resp, **kwargs):
        ip = kwargs.pop("ip", None)
        if not is_ip(ip):
            return {}
        return IpaddressApi().get(primiry_id=ip)

    def update(self, req, data, resp, **kwargs):
        ip = kwargs.pop("ip", None)
        if not is_ip(ip):
            return {}
        if "host_id" in data.keys():
            HostApi().valitdae_host(data["host_id"])

        return IpaddressApi().update(primiry_id=ip, data=data)

    def delete(self, req, data, resp, **kwargs):
        ip = kwargs.pop("ip", None)
        if not is_ip(ip):
            return {}
        return IpaddressApi().delete(primiry_id=ip)


class IpLocalHandler(BaseResponse):
    '''
    主机本地ip， 由主机上报
    由于实际可能存在HA IP, （例如keepalive）, ip可能在多个主机之间移动；
    因此该功能， 需更新ip host信息， 对于已经存在的graph 数据依然有效，不应做清理
    '''
    allowed_methods = ["POST"]

    def list(self, req, data, resp, **kwargs):
        return IpaddressApi().query(filter=data, **kwargs)

    def on_ip_create(self, ip, uuid):
        return IpaddressApi().insert(data={"ip": ip, "host_id": uuid})

    def on_ip_update(self, ip, uuid):
        return IpaddressApi().update(primiry_id=ip, data={"host_id": uuid})

    def create(self, req, data, resp, **kwargs):
        if not data.get("id"):
            raise ValueError("注册信息缺少主机UUID")
        if not data.get("ip"):
            raise ValueError("注册信息缺少IP")
        uuid = data["id"]
        ipaddress = data["ip"]
        _ipdata = IpaddressApi().get(primiry_id=ipaddress)
        if _ipdata:
            if _ipdata.get("host_id") != uuid:
                self.on_ip_update(ip=ipaddress, uuid=uuid)
        else:
            self.on_ip_create(ip=ipaddress, uuid=uuid)

        return 1, ipaddress
