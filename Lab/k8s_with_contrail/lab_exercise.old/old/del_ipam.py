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
	if len(arg1) != 7:
		print("usage : set_rt.py -h <api_server_host> -vn <vn name> -ns <namespace name>")
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
		#if "-pn" in t1:
		#	sample+=1
		if "-ns" in t1:
			sample+=1
		if sample != 3:
			print("missing argument")
			return 0
		else:
			d1={}
			for i in t1:
				d1[i.replace("-","")]=arg1[arg1.index(i) + 1]
			return d1




def del_ipam(d1):
    vnc=vnc_api.VncApi(api_server_host=d1['h'])
    URL="http://" + d1['h'] + ":8082/network-ipams"
    ipam_list=requests.get(URL).json()
    for i in ipam_list['network-ipams']:
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



# Main program
d1=check_arg(sys.argv)
if d1:
	print("d1",d1)
	del_ipam(d1)
else:
	print("missing argument")
