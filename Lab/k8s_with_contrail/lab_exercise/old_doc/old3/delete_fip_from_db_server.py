#!/usr/bin/env python3
# to delete floating ip from db server
from vnc_api import vnc_api
import requests
import sys
import uuid

#required parameter
host="172.16.11.10"
ns="ns-user4"
vn="vn-external4"
pool_name="pool-vn-external4"
server1="dbserver4"



URL="http://" + host + ":8082/virtual-machine-interfaces"
vmi_list=requests.get(URL).json()
# print("vmi_list", vmi_list)
href=''
vmi_id=''
for i in vmi_list['virtual-machine-interfaces']:
    if ns in i['fq_name'][1] and server1 in i['fq_name'][2]:
        href=i['href']
        vmi_id=i['uuid']
        break
if vmi_id:
    # fip_list=requests.get(href).json()['virtual-machine-interface']['floating_ip_back_refs']
    vmi_data=requests.get(href).json()['virtual-machine-interface']
    if 'floating_ip_back_refs' in vmi_data.keys():
    #print('fip list',fip_list)
        fip_href=''
        for i in vmi_data['floating_ip_back_refs']:
            if ns in i['to'][1] and vn in i['to'][2] and pool_name in i['to'][3]:
                fip_href=i['href']
                break
        if fip_href:
            print("fip href",fip_href)
            print("deleting  from pod ", vmi_id)
            r=requests.delete(fip_href)
            print("Result ",r)
    else:
        print("no FIP assigned to pod ",vmi_id)