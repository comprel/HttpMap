from lib.ip import is_ip
from core.controller import BaseResponse
from dbs.host.api import HostApi
from dbs.host.api import IpaddressApi


class IpAddressHandler(BaseResponse):
    '''
    主机ip 不提供创建数据功能， 创建由上报数据进行
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
