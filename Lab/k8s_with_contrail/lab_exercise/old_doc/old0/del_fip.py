#!/usr/bin/env python3
import requests
from vnc_api import vnc_api
api_server_host='172.16.11.10'
api_username='admin'
api_password='contrail123'
vn='vn-external'
ns='ns-user-1'
pool_name='pool-vn-external'

# vnc=vnc_api.VncApi(api_server_host=api_server_host,username=api_username,password=api_password)
vnc=vnc_api.VncApi(api_server_host=api_server_host)
fip_list=vnc.floating_ip_pools_list()
href=''
uuid=''
for i in fip_list['floating-ip-pools']:
	if ns in i['fq_name'][1] and vn in i['fq_name'][2] and pool_name in i['fq_name'][3]:
		# print("yes")
		href=i['href']
		uuid=i['uuid']
		break
if href and uuid:
    print("href {}".format(href))
    print("uuid {}".format(uuid))
    print("deleting floating ip {}".format(pool_name))
    r=requests.delete(href)
    print("result",r)


