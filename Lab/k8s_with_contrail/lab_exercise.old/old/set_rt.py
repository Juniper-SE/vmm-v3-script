#!/usr/bin/env python3
# to set route target, router_external status, and floating ip pools
import requests
from vnc_api import vnc_api
import sys
#api_server_host='172.16.11.10'
#api_username='admin'
#api_password='contrail123'
#required parameters
#vn='vn-external1'
#ns='default'
#rt_export="64512:10001"
#rt_import="64512:10000"
#pool_name='pool-vn-external1'



def check_arg(arg1):
	if len(arg1) != 13:
		print("usage : set_rt.py -h <api_server_host> -vn <vn name> -ns <namespace name> -pn <floating ip pool name> -rte <route target_export> -rti <route target import>")
		return 0
	else:
		t1=[]
		i=1
		while i < len(arg1):
			t1.append(arg1[i])
			i+=2
		sample=0
		if "-h" in t1:
			sample+=1
		if "-vn" in t1:
			sample+=1
		if "-pn" in t1:
			sample+=1
		if "-ns" in t1:
			sample+=1
		if "-rte" in t1:
			sample+=1
		if "-rti" in t1:
			sample+=1
		if sample != 6:
			print("missing argument")
			return 0
		else:
			d1={}
			for i in t1:
				d1[i.replace("-","")]=arg1[arg1.index(i) + 1]
			return d1

def set_rt_fip(d1):
	vnc=vnc_api.VncApi(api_server_host=d1['h'])
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
		k8s_vn='k8s-' + d1['vn'] + '-pod-network'
		project='k8s-' + d1['ns']
		print("network {}, project {}".format(k8s_vn,project))
		# setting external and route target
		print("set route external and route target")
		vn_result=vnc.virtual_network_read(fq_name=['default-domain',project,k8s_vn])
		route_target=vnc_api.RouteTargetList(['target:' + d1['rti']])
		vn_result.set_import_route_target_list(route_target)
		route_target=vnc_api.RouteTargetList(['target:' + d1['rte']])
		vn_result.set_export_route_target_list(route_target)
		vn_result.set_router_external(True)
		vnc.virtual_network_update(vn_result)
		# creating floating ip pools
		print("creating floating ip pools")
		FIpool = vnc_api.FloatingIpPool(name = d1['pn'],parent_obj = vn_result)
		vnc.floating_ip_pool_create(FIpool)
		tenant = vnc.project_read(fq_name = ['default-domain', project])
		tenant.add_floating_ip_pool(FIpool)
		vnc.project_update(tenant)
	else:
		print("virtual network {} does not exist".format(d1['vn']))

# Main program
d1=check_arg(sys.argv)
if d1:
	print("d1",d1)
	set_rt_fip(d1)
else:
	print("missing argument")
