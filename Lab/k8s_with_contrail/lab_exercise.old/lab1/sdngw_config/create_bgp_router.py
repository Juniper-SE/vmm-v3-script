#!/usr/bin/env python3
# to create BGP router
# to install library pip3 install contrail-api-client
import requests
from vnc_api import vnc_api
# api_server_host='172.16.10.2'
api_server_host='127.0.0.1'
# api_server_host='10.1.1.180'
api_username='admin'
api_password='contrail123'
# required parameter
bgp_router_address="172.16.255.1"
# bgp_router_address="10.1.255.1"
router_name="sdngw"
peer_node="master"
asn=64512
# vnc=vnc_api.VncApi(api_server_host=api_server_host,username=api_username,password=api_password)
vnc=vnc_api.VncApi(api_server_host=api_server_host)
routing_instance=vnc.routing_instance_read(fq_name=['default-domain','default-project', 'ip-fabric', '__default__'])
print(routing_instance)
bgp_parameters={
    "vendor": "juniper",
    "admin_down": False,
    "local_autonomous_system": None,
    "auth_data": None,
    "address": bgp_router_address,
    "autonomous_system": asn,
    "router_type": "router",
    "identifier": bgp_router_address,
    "hold_time": 90,
    "port": 179,
    "address_families": {
        "family": [
            "inet-vpn",
            "inet6-vpn",
            "route-target",
            "e-vpn"
        ]
    }
}
fq_name=["default-domain","default-project","ip-fabric","__default__",router_name]
bgp_peer={ "to": [ "default-domain", "default-project","ip-fabric","__default__",peer_node] }
print("bgp parameters", bgp_parameters)
bgp_router = vnc_api.BgpRouter(fq_name=fq_name,name = router_name,parent_obj = routing_instance,bgp_router_parameters=bgp_parameters,bgp_router_refs=[bgp_peer])
print("Creating BGP router ")
vnc.bgp_router_create(bgp_router)
#routing_instance.bgp_router_add(bgp_router)
#vnc.routing_instance_update(routing_instance)
