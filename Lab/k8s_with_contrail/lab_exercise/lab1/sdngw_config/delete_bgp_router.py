#!/usr/bin/env python3
# to delete BGP peer.
import requests
from vnc_api import vnc_api
api_server_host='127.0.0.1'
api_username='admin'
api_password='contrail123'
# required parameter
router_name="sdngw"
# vnc=vnc_api.VncApi(api_server_host=api_server_host,username=api_username,password=api_password)
vnc=vnc_api.VncApi(api_server_host=api_server_host)
vn_network_list=vnc.bgp_routers_list()
href=''
uuid=''
for i in vn_network_list['bgp-routers']:
	if router_name in i['fq_name'][4]:
		# print("yes")
		href=i['href']
		uuid=i['uuid']
		break
if href:
    print("bgp router ",href)
    print("Delete bgp router")
    r=requests.delete(href)
    print("result ",r)
