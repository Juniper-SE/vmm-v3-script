#!/usr/bin/env python3
# to delete route target, remove router_external status and remove floating ip pools 
from vnc_api import vnc_api
import requests
import sys
#api_server_host='172.16.11.10'
#api_username='admin'
#api_password='contrail123'
#requred parameters
#vn='vn-external1'
#ns='default'
#pool_name='pool-vn-external1'
# vnc=vnc_api.VncApi(api_server_host=api_server_host,username=api_username,password=api_password)
d1=check_arg(sys.arg)
if d1:
	del_rt_fip(d1)
else:
	print("missing argument")

def check_arg(d1).

def del_rt_fip(d1):
	vnc=vnc_api.VncApi(api_server_host=d1['api_server_host'])
	vn_network_list=vnc.virtual_networks_list()
	href=''
	uuid=''
	for i in vn_network_list['virtual-networks']:
		if d1['ns'] in i['fq_name'][1] and d1['vn'] in i['fq_name'][2]:
			# print("yes")
			href=i['href']
			uuid=i['uuid']
			break
	if href and uuid:
		print("virtual network {} in namespace {}".format(d1['vn'],d1['ns']))
		print("href {}".format(href))
		print("uuid {}".format(uuid))
		k8s_vn='k8s-'+ d1['vn'] + '-pod-network'
		project='k8s-' + d1['ns']
		print("network {}, project {}".format(k8s_vn,project))
		tenant = vnc.project_read(fq_name = ['default-domain', project])
		vn_result=vnc.virtual_network_read(fq_name=['default-domain',project,k8s_vn])
		route_target=None
		#vn_result.set_route_target_list(None)
		vn_result.set_export_route_target_list(None)
		vn_result.set_import_route_target_list(None)
		vn_result.set_router_external(None)
		#vn_result.set_floating_ip_pools(None)
		print("delete router external and route target")
		vnc.virtual_network_update(vn_result)
		fipool = vnc.floating_ip_pool_read(fq_name=['default-domain',project,k8s_vn,pool_name])
		tenant = vnc.project_read(fq_name = ['default-domain', project])
		tenant.del_floating_ip_pool(fipool)
		vnc.project_update(tenant)
		#vnc.floating_ip_pool_delete(fipool)
		URL="http://" + api_server_host + ":8082/floating-ip-pools"
		fipool_list=requests.get(URL).json()
		for i in fipool_list['floating-ip-pools']:
			if d1['ns'] in i['fq_name'][1] and d1['vn'] in i['fq_name'][2] and d1['pool_name'] in i['fq_name'][3]:
				href=i['href']
				uuid=i['uuid']
				break
		if href:
			print("deleting floating ip pool ",href)
			r=requests.delete(href)
			print("result ",r)
		URL="http://" + api_server_host + ":8082/network-ipams"
		ipam_list=requests.get(URL).json()
		for i in fipool_list['network-ipams']:
			if d1['ns'] in i['fq_name'][1] and d1['vn'] in i['fq_name'][2]:
				href=i['href']
				uuid=i['uuid']
				break
		if href:
			print("deleting network ipam ",href)
			r=requests.delete(href)
			print("result ",r)
		
	else:
		print("virtual network {} does not exist".format(d1['vn']))
