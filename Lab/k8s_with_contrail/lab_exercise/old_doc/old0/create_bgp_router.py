#!/usr/bin/env python3
from vnc_api import vnc_api
import requests
import yaml
api_server_host='172.16.11.10'
api_username='admin'
api_password='contrail123'
asn=64512
ipaddr="172.16.255.255"
vendorid="juniper"
routername="vmx1"
peer="node0"
bgp1='''---
bgp-router:
    bgp_router_parameters:
        address: {0}
        address_families:
            - inet-vpn
            - inet6-vpn
            - route-target
            - evpn
        identifier: {0}
        autonomous_system : {1}
        router_type: router
        vendor: {2}
    bgp_router_refs:
        - to:
            - default-domain
            - default-project
            - ip-fabric
            - {3}
    display_name: {4}
    fq_name:
        - default-domain
        - default-project
        - ip-fabric
        - __default__
        - {4}
    name: {4}
'''.format(ipaddr,asn,vendorid,peer,routername)
bgp_data=yaml.full_load(bgp1)
print(bgp_data)
URL="http://" + api_server_host + ":8082/bgp-routers"
r=requests.post(URL,data=bgp_data)
print("result ",r)