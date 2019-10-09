from core.route import url
from controller.host.host import HostHandler
from controller.host.host import HostIdHandler
from controller.host.register import HostRegister
from controller.host.register import HostUnRegister
from controller.host.ipaddress import IpAddressHandler
from controller.host.ipaddress import IpAddressIdHandler
from controller.host.ipaddress import IpLocalHandler
from controller.host.graph import GraphAllHandler
from controller.host.graph import GraphNodeHandler
from controller.host.graph import GraphRealtionHandler

add_route = [
    url("/api/v1/host/host", HostHandler()),
    url("/api/v1/host/host/{uuid}", HostIdHandler()),
    url("/api/v1/host/ipaddress", IpAddressHandler()),
    url("/api/v1/host/ipaddress/{ip}", IpAddressIdHandler()),
    url("/api/v1/host/localipaddress", IpLocalHandler()),
    url("/api/v1/host/register", HostRegister()),
    url("/api/v1/host/register/{uuid}", HostUnRegister()),

    url("/api/v1/host/graph", GraphAllHandler()),
    url("/api/v1/host/graph/{uuid}", GraphNodeHandler()),
    url("/api/v1/host/graph/{uuid1}/{uuid2}", GraphRealtionHandler()),
]
