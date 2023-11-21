#!/usr/bin/env python3
# to set and delete  route target, router_external status, floating ip pools and ipam

import requests, os, yaml
from vnc_api import vnc_api

def check_arg(arg1):
	condition = False
	command_list=['set_rt','del_rt','del_ipam']
	d1={}
	if len(arg1) == 2 and arg1[1] in command_list:
		filename="./lab.yaml"
		cmd=arg1[1]
	elif len(arg1) == 4 and arg1[1] in command_list and '-c' in arg1[2]:
		filename=arg1[3]
		cmd=arg1[1]
	elif len(arg1) == 4 and arg1[3] in command_list and '-c' in arg1[1]:
		filename=arg1[2]
		cmd=arg1[3]
	else:
		print("usage : config_lab.py <command> -c <config_file>")
		print("<command> :")
		print("   - set_rt")
		print("   - del_rt")
		print("   - del_ipam")
		return None
	try:
		f1=open(filename)
		d1=yaml.load(f1,Loader=yaml.FullLoader)
		d1['command']=cmd
		#print("d1 ",d1)
		return d1
	except IOError:
		print("Filename {} is not available or can't be read, please create one or change the privilige".format(filename))
		return None

def get_vn_info(d1):
	vnc=vnc_api.VncApi(api_server_host=d1['api_server_host'])
	vn_network_list=vnc.virtual_networks_list()
	retval={}
	for i in vn_network_list['virtual-networks']:
		if d1['namespace'] in i['fq_name'][1] and d1['virtual_network'] in i['fq_name'][2]:
			# print("yes")
			retval['href']=i['href'] 
			retval['uuid']= i['uuid'] 
			break
	return retval

def get_pool_info(d1):
	retval={}
	URL="http://" + d1['api_server_host'] + ":8082/floating-ip-pools"
	fipool_list=requests.get(URL).json()
	for i in fipool_list['floating-ip-pools']:
		if d1['namespace'] in i['fq_name'][1] and d1['virtual_network'] in i['fq_name'][2] and d1['pool_name'] in i['fq_name'][3]:
			retval['href']=i['href'] 
			retval['uuid']= i['uuid'] 
			break
	return retval

def get_ipam_info(d1):
	retval={}
	URL="http://" + d1['api_server_host'] + ":8082/network-ipams"
	ipam_list=requests.get(URL).json()
	for i in ipam_list['network-ipams']:
		if d1['namespace'] in i['fq_name'][1] and d1['virtual_network'] in i['fq_name'][2]:
			retval['href']=i['href'] 
			retval['uuid']= i['uuid'] 
			break
	return retval


def set_rt_fip(d1):
	vn_info=get_vn_info(d1)
	print("vn_info" ,vn_info)
	#vn_info=None
	if vn_info:
		print("virtual network {} in namespace {}".format(d1['virtual_network'],d1['namespace']))
		print("href {}".format(vn_info['href']))
		print("uuid {}".format(vn_info['uuid']))
		k8s_vn='k8s-' + d1['virtual_network'] + '-pod-network'
		project='k8s-' + d1['namespace']
		print("network {}, project {}".format(k8s_vn,project))
		# setting external and route target
		print("set route external and route target")
		vnc=vnc_api.VncApi(api_server_host=d1['api_server_host'])
		vn_result=vnc.virtual_network_read(fq_name=['default-domain',project,k8s_vn])
		route_target=vnc_api.RouteTargetList(['target:' + d1['route_target_import']])
		vn_result.set_import_route_target_list(route_target)
		route_target=vnc_api.RouteTargetList(['target:' + d1['route_target_export']])
		vn_result.set_export_route_target_list(route_target)
		vn_result.set_router_external(True)
		vnc.virtual_network_update(vn_result)
		# creating floating ip pools
		print("creating floating ip pools")
		FIpool = vnc_api.FloatingIpPool(name = d1['pool_name'],parent_obj = vn_result)
		vnc.floating_ip_pool_create(FIpool)
		tenant = vnc.project_read(fq_name = ['default-domain', project])
		tenant.add_floating_ip_pool(FIpool)
		vnc.project_update(tenant)
	else:
		print("virtual network {} does not exist".format(d1['virtual_network']))


def del_rt_fip(d1):
	vn_info=get_vn_info(d1)
	if vn_info:
		print("virtual network {} in namespace {}".format(d1['virtual_network'],d1['namespace']))
		print("href {}".format(vn_info['href']))
		print("uuid {}".format(vn_info['uuid']))
		k8s_vn='k8s-' + d1['virtual_network'] + '-pod-network'
		project='k8s-' + d1['namespace']
		print("network {}, project {}".format(k8s_vn,project))
		vnc=vnc_api.VncApi(api_server_host=d1['api_server_host'])
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
		fipool = vnc.floating_ip_pool_read(fq_name=['default-domain',project,k8s_vn,d1['pool_name']])
		tenant = vnc.project_read(fq_name = ['default-domain', project])
		tenant.del_floating_ip_pool(fipool)
		vnc.project_update(tenant)
		fip_pool=get_pool_info(d1)
		if fip_pool:
			print("deleting floating ip pool ",fip_pool['href'])
			r=requests.delete(fip_pool['href'])
			print("result ",r)
	else:
		print("floating ip  {} does not exist".format(d1['pool_name']))

def del_ipam(d1):
    ipam_info=get_ipam_info(d1)
    if ipam_info:
        print("deleting network ipam ",ipam_info['href'])
        r=requests.delete(ipam_info['href'])
        print("result ",r)
        
    else:
        print("IPAM for virtual network  {} does not exist".format(d1['virtual_network']))


