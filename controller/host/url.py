from core.route import url
from controller.host.host import HostHandler
from controller.host.host import HostIdHandler
from controller.host.register import HostRegister
from controller.host.register import HostUnRegister
from controller.host.ipaddress import IpAddressHandler
from controller.host.ipaddress import IpAddressIdHandler

add_route = [
    url("/api/v1/host/host", HostHandler()),
    url("/api/v1/host/host/{uuid}", HostIdHandler()),
    url("/api/v1/host/ipaddress", IpAddressHandler()),
    url("/api/v1/host/ipaddress/{ip}", IpAddressIdHandler()),
    url("/api/v1/host/register", HostRegister()),
    url("/api/v1/host/register/{uuid}", HostUnRegister()),
]
