#!/usr/bin/env python3
import requests
from vnc_api import vnc_api
api_server_host='172.16.11.10'
api_username='admin'
api_password='contrail123'
vn='vn-external'
ns='ns-user-1'
rt="64512:10001"
pool_name='pool-vn-external'
#vnc=vnc_api.VncApi(api_server_host=api_server_host)
#FIPool_list=vnc.floating_ip_pools_list()
URL="http://" + api_server_host + ":8082/floating-ip-pools"
FIPool_list=requests.get(URL).json()
href=''
uuid=''
#print("FIPool",FIPool_list)
for i in FIPool_list['floating-ip-pools']:
    if ns in i['fq_name'][1] and vn in i['fq_name'][2] and pool_name in i['fq_name'][3]:
        href=i['href']
        uuid=i['uuid']
        break
if href or uuid:
    print("href ",href)