#!/usr/bin/env python3
# to set route target, router_external status, and floating ip pools
import requests
from vnc_api import vnc_api
api_server_host='172.16.11.10'
api_username='admin'
api_password='contrail123'
#required parameters
vn='vn-external1'
ns='default'
rt_export="64512:10001"
rt_import="64512:10000"
pool_name='pool-vn-external1'
if check_arg(sys.arg):
# vnc=vnc_api.VncApi(api_server_host=api_server_host,username=api_username,password=api_password)
	d1={ 'api_host_host' : api_server_host, 'api_username' : api_username,'api_password' : api_password
	'vn' : vn, 'ns' : ns, 'rt_export': rt_export, 'rt_import' : rt_import
	}
	set_rt_fip(d1)
else:
	print("missing argument")

def set_rt_fip(d1):
	vnc=vnc_api.VncApi(api_server_host=d1['api_server_host'])
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
		print("virtual network {} in namespace {}".format(d1['vn'],d1['ns']))
		print("href {}".format(href))
		print("uuid {}".format(uuid))
		k8s_vn='k8s-' + d1['vn'] + '-pod-network'
		project='k8s-' + d1['ns']
		print("network {}, project {}".format(k8s_vn,project))
		# setting external and route target
		print("set route external and route target")
		vn_result=vnc.virtual_network_read(fq_name=['default-domain',project,k8s_vn])
		route_target=vnc_api.RouteTargetList(['target:' + d1['rt_import']])
		vn_result.set_import_route_target_list(route_target)
		route_target=vnc_api.RouteTargetList(['target:' + d1['rt_export']])
		vn_result.set_export_route_target_list(route_target)
		vn_result.set_router_external(True)
		vnc.virtual_network_update(vn_result)
		# creating floating ip pools
		print("creating floating ip pools")
		FIpool = vnc_api.FloatingIpPool(name = pool_name,parent_obj = vn_result)
		vnc.floating_ip_pool_create(FIpool)
		tenant = vnc.project_read(fq_name = ['default-domain', project])
		tenant.add_floating_ip_pool(FIpool)
		vnc.project_update(tenant)
	else:
		print("virtual network {} does not exist".format(d1['vn']))
