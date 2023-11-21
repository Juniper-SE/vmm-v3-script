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

def check_arg(arg1):
	if len(arg1) != 9:
		print("usage : set_rt.py -h <api_server_host> -vn <vn name> -ns <namespace name> -pn <floating ip pool name>")
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
		if sample != 4:
			print("missing argument")
			return 0
		else:
			d1={}
			for i in t1:
				d1[i.replace("-","")]=arg1[arg1.index(i) + 1]
			return d1




def del_rt_fip(d1):
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
		fipool = vnc.floating_ip_pool_read(fq_name=['default-domain',project,k8s_vn,d1['pn']])
		tenant = vnc.project_read(fq_name = ['default-domain', project])
		tenant.del_floating_ip_pool(fipool)
		vnc.project_update(tenant)
		#vnc.floating_ip_pool_delete(fipool)
		URL="http://" + d1['h'] + ":8082/floating-ip-pools"
		fipool_list=requests.get(URL).json()
		for i in fipool_list['floating-ip-pools']:
			if d1['ns'] in i['fq_name'][1] and d1['vn'] in i['fq_name'][2] and d1['pn'] in i['fq_name'][3]:
				href=i['href']
				uuid=i['uuid']
				break
		if href:
			print("deleting floating ip pool ",href)
			r=requests.delete(href)
			print("result ",r)
		#URL="http://" + d1['h'] + ":8082/network-ipams"
		#ipam_list=requests.get(URL).json()
		#for i in ipam_list['network-ipams']:
		#	if d1['ns'] in i['fq_name'][1] and d1['vn'] in i['fq_name'][2]:
		#		href=i['href']
		#		uuid=i['uuid']
		#		break
		#if href:
		#	print("deleting network ipam ",href)
		#	r=requests.delete(href)
		#	print("result ",r)
		
	else:
		print("virtual network {} does not exist".format(d1['vn']))



# Main program
d1=check_arg(sys.argv)
if d1:
	print("d1",d1)
	del_rt_fip(d1)
else:
	print("missing argument")
