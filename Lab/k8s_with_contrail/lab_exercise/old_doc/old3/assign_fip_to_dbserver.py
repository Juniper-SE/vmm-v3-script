#!/usr/bin/env python3
# to assign floating ip pool to server1 
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


#new variable
project="k8s-" + ns
vn_name="k8s-"+ vn + "-pod-network"

vnc=vnc_api.VncApi(api_server_host=host)
id = str(uuid.uuid4())
pool = vnc.floating_ip_pool_read(fq_name = ['default-domain', project, vn_name, pool_name])
fip = vnc_api.FloatingIp(name = id, parent_obj = pool)
#fip.uuid = id
fip_id=vnc.floating_ip_create(fip)
href="http://" + host + ":8082/floating-ip/" + fip_id
fip_ip=requests.get(href).json()['floating-ip']['floating_ip_address']
print("href ",href)
print("uuid ",fip_id) 
print("floating ip ", fip_ip)
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
    print("associating VMI {} with floating ip {}".format(vmi_id,fip_ip))
    vmi = vnc.virtual_machine_interface_read(id = vmi_id)
    tenant = vnc.project_read(fq_name = ['default-domain', project])
    fip = vnc.floating_ip_read(id = fip_id)
    fip.add_project(tenant)
    fip.add_virtual_machine_interface(vmi)
    vnc.floating_ip_update(fip)
