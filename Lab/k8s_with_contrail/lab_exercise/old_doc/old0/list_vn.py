#!/usr/bin/env python3
from vnc_api import vnc_api
api_server_host='172.16.11.10'
api_username='admin'
api_password='contrail123'
vn='vn-external'
ns='ns-user-1'
# vnc=vnc_api.VncApi(api_server_host=api_server_host,username=api_username,password=api_password)
vnc=vnc_api.VncApi(api_server_host=api_server_host)
vn_network_list=vnc.virtual_networks_list()
href=''
uuid=''
for i in vn_network_list['virtual-networks']:
	if ns in i['fq_name'][1] and vn in i['fq_name'][2]:
		# print("yes")
		href=i['href']
		uuid=i['uuid']
		break
if href and uuid:
	print("virtual network {} in namespace {}".format(vn,ns))
	print("href {}".format(href))
	print("uuid {}".format(uuid))

k8s_vn='k8s-'+ vn + '-pod-network'
project='k8s-' + ns
print("network {}, project {}".format(k8s_vn,project))


result=vnc.virtual_network_show(fq_name=['default-domain',project,k8s_vn])
print("result {}".format(result))

