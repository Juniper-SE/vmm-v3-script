#!/usr/bin/env python3
# this library is used to create configuration files to run VM (Centos/Ubuntu) and Junos (VMX/VQFX) on VMM (juniper internal cloud)
# created by mochammad irzan irzan@juniper.net
# 20 october 2019

# 24 July 2021, updated for VMM 3.0 (not backward compatible with previous version of VMM)

# 13 augustus 2025, updated with kea-dhcp4-server on node GW

# 4 sept 2025 : removing ssh key from the script

import param1
import sys
import os
import shutil
import paramiko
from jinja2 import Template
import shutil

import yaml
import pexpect
import pprint
from scp import SCPClient
import random
import subprocess
from passlib.hash import md5_crypt
import time
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519
from cryptography.hazmat.backends import default_backend

#from pathlib import Path
#import time
#import pathlib
# from jnpr.junos import Device
# from jnpr.junos.utils.config import Config

# def get_vmm_capacity(d1):
# 	vmm_cap = {}
# 	print("Checking capacity")
# 	for vmm in param1.vmm_servers:
# 		server=f"{vmm}-vmm.englab.juniper.net"
# 		print(f"server : {server}, ", end=" ")
# 		ssh=paramiko.SSHClient()
# 		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 		ssh.connect(hostname=server,username=d1['pod']['user'],password=d1['pod']['vmmpassword'])
# 		cmd1 = "vmm capacity -g vmm-default"
# 		stdin, stdout, stderr = ssh.exec_command(cmd1, get_pty=True)
# 		for line in iter(stdout.readline, ""):
# 			if "Total" in line:
# 				c1 = int(line.split(":")[1])
# 			if "Free" in line:
# 				f1 = int(line.split(":")[1])
# 		# vmm_cap[vmm]={"total" : c1, "free": f1}
# 			# print(line, end="")
# 		ssh.close()
# 		print(f"total {c1}, free {f1}")
# 	# print("%10s %6d %5d" % ("server","total","free"))
# 	# for vmm in vmm_cap.keys():
# 	# 	print("%10s %5d %5d" % (vmm,vmm_cap[vmm]['total'],vmm_cap[vmm]['free']))
	
def generate_wireguard_keys():
    """
    Generate a WireGuard private & public key
    Requires that the 'wg' command is available on PATH
    Returns (private_key, public_key), both strings
    """
    #print("function generate_wireguar_keys")
    privkey = subprocess.check_output("/opt/homebrew/bin/wg genkey", shell=True).decode("utf-8").strip()
    pubkey = subprocess.check_output(f"echo '{privkey}' | /opt/homebrew/bin/wg pubkey", shell=True).decode("utf-8").strip()
    #print(privkey, pubkey)
    return [privkey, pubkey]

def get_wg_config(d1):
	dummy1={}
	gw_t1="""
[Interface]
PrivateKey={{gw_key.0}}
Address={{gw_ip}}
ListenPort=443
[Peer]
PublicKey={{ws_key.1}}
AllowedIPs={{allowed_ip_gw}}
"""
	ws_t1="""
[Interface]
PrivateKey={{ws_key.0}}
Address={{ws_ip}}
[Peer]
PublicKey={{gw_key.1}}
EndPoint={{eth0_gw}}:443
AllowedIPs={{allowed_ip_ws}}
"""
	
	#print("in the function")
	#print(d1.keys())
	try:
		if 'wg' in d1.keys():
			#print("wireguard is configured")
			result1 = subprocess.check_output("/opt/homebrew/bin/wg", shell=True).decode("utf-8").strip()
			if 'tunnel_ip' not in d1['wg'].keys():
				dummy1['gw_ip'] = '192.168.199.0/31;fc00:dead:beef:ffcc::1000:0/127'
				dummy1['ws_ip'] = '192.168.199.1/31;fc00:dead:beef:ffcc::1000:1/127'
			else:
				dummy1['gw_ip'] = d1['wg']['tunnel_ip']['gw_ip']
				dummy1['ws_ip'] = d1['wg']['tunnel_ip']['ws_ip']
			
			dummy1['gw_key'] = generate_wireguard_keys()
			dummy1['ws_key'] = generate_wireguard_keys()
			# print(dummy1['gw_key'],dummy1['ws_key'])
			# print("after generat3 keys")
			# print(len(dummy1['gw_ip'].split(';')))
			if len(dummy1['gw_ip'].split(';')) == 1:
				
				dummy1['allowed_ip_gw']=f"{dummy1['ws_ip'].split('/')[0]}/32"
			else:
				#print("checkpoint 2")
				t1 = dummy1['ws_ip'].split(';')
				#print(t1)
				dummy1['allowed_ip_gw']=f"{t1[0].split('/')[0]}/32,{t1[1].split('/')[0]}/128"
				#print(dummy1['allowed_ip_gw'])

			if len(dummy1['ws_ip'].split(';')) == 1:
				dummy1['allowed_ip_ws']=f"{dummy1['gw_ip'].split('/')[0]}/32"
			else:
				#dummy1['allowed_ip_ws']=f"{dummy1['gw_ip'].split[';'][0].split('/')[0]}/32,{dummy1['gw_ip'].split[';'][1].split('/')[0]}/128"
				t1 = dummy1['gw_ip'].split(';')
				#print(t1)
				dummy1['allowed_ip_ws']=f"{t1[0].split('/')[0]}/32,{t1[1].split('/')[0]}/128"
			# dummy1['allowed_ip_ws']=f"{dummy1['gw_ip'].split('/')[0]}/32"
			print(dummy1)
			for i in d1['wg']['prefix_allowed']:
				dummy1['allowed_ip_ws']+=f",{i}"
			print("getting node gw eth0 ip address")
			dummy1['eth0_gw']=get_ip_vm(d1,'gw')
			# dummy1['allowd_ip_wg'].append(dummy1['ws_ip'].split('/')[0])
			#print(dummy1)
			dummy1['gw_ip']=dummy1['gw_ip'].replace(';',',')
			dummy1['ws_ip']=dummy1['ws_ip'].replace(';',',')
			gw_config=Template(gw_t1).render(dummy1)
			print(gw_config)
			ws_config=Template(ws_t1).render(dummy1)
			print(ws_config)

			print("writing wireguard configuration node gw")
			print("upload file tmp/wg0_gw.conf to node gw, /etc/wireguard/wg0.conf, and restart wireguard service")
			with open('tmp/wg0_gw.conf','w') as f1:
				f1.write(gw_config)
			print("writing wireguard configuration for your workstation")
			print("upload file tmp/wg0_ws.conf the local wiregard directory, i.e /usr/local/etc/wireguard/wg0.conf, and restart wireguard service")
			with open('tmp/wg0_ws.conf','w') as f1:
				f1.write(ws_config)
		else:
			print("wireguard is not configured")
	except:
		print("wireguard is not installed  on your system")

def print_data(d1):
	print("printing data")
	print("-------------")
	print(yaml.dump(d1))

def num_link_with_ip(d1):
	retval4=0
	retval6=0
	for i in d1['fabric']['topology']:
		if i[0] & param1.mask_ipv4:
			retval4+=1
		if i[0] & param1.mask_ipv6:
			retval6+=1
	return retval4, retval6

def read_config(config):
	d1={}
	config_file = config['config_file']
	status=0
	try:
		# f1=open(config_file)
		# d1=yaml.load(f1,Loader=yaml.FullLoader)
		# f1.close()
		with open(config_file) as f1:
			d1=yaml.load(f1,Loader=yaml.FullLoader)
		add_ssh_key(d1)
		add_path(d1,config['path'])
		add_os(d1)
		if 'fabric' in d1.keys():
			#num_link = len(d1['fabric']['topology'])
			num_link, num_link6 = num_link_with_ip(d1)
			# print(f"num_link {num_link}")
			if num_link == 0:
				#print("num_link 0")
				status = 0
			elif (num_link > 0) and ('subnet' not in d1['fabric'].keys()):
				print("subnet for fabric is not defined on lab.yaml")
				exit(1)
			elif (num_link > 0) and ('subnet' in d1['fabric'].keys()):
				pref_len = 32 - int(d1['fabric']['subnet'].split('/')[1])
				#pref_len6 = 128 - int(d1['fabric']['subnet6'].split('/')[1])
				num_subnet = int( (2 **  pref_len) / 2)
				#num_subnet6 = int( (2 **  pref_len6) / 2)
				#print(f"num_link {num_link} num_subnet {num_subnet} num_subnet6 {num_subnet6}")
				#exit(1)
				if (num_link > num_subnet):
					print(f"not enough ip address for fabric link\nnum of link {num_link}, num of subnet {num_subnet}" )
					exit(1)
				elif check_ip(d1):
					print("wrong subnet allocation")
					print(f"subnet {d1['fabric']['subnet'].split('/')[0]} can't be used with prefix {d1['fabric']['subnet'].split('/')[1]}")
				#elif not check_vm(d1):
				#	print("number of VM on topology doesn't match with on configuration")
				else:
					status=1
			# if num_link6 > 0:
			# 	if 'subnet6' in d1['fabric'].keys():
			# 		pref_len6 = 128 - int(d1['fabric']['subnet6'].split('/')[1])
			# 		num_subnet6 = int( (2 **  pref_len6) / 2)
			# 	#print(f"num_link {num_link} num_subnet {num_subnet} num_subnet6 {num_subnet6}")
			# 	#exit(1)
			# 		if (num_link6 > num_subnet6):
			# 			print(f"not enough ip address for fabric link\nnum of link {num_link}, num of subnet {num_subnet}" )
			# 			exit(1)
			# 		# elif check_ip(d1):
			# 		# 	print("wrong subnet allocation")
			# 		# 	print(f"subnet {d1['fabric']['subnet'].split('/')[0]} can't be used with prefix {d1['fabric']['subnet'].split('/')[1]}")
			# 		#elif not check_vm(d1):
			# 		#	print("number of VM on topology doesn't match with on configuration")
			# 	status=1
			# if status:
			create_config_interfaces(d1)
		# pprint.pprint(d1)
		# exit()
		change_gateway4(d1)
		change_ztp(d1)
		change_loopback(d1)
		adpassword_env=os.getenv('ADPASSWORD')
		#print(f"adpassword ${adpassword_env}")
		user_env=os.getenv('USER')
		vmmpassword_env=os.getenv('VMMPASSWORD')
		# if 'jumpserver' in d1['pod'].keys():
		# 	if adpassword_env:
		# 		d1['pod']['adpassword'] = adpassword_env
		# 	else:
		# 		if 'adpassword' not in d1['pod']: 
		# 			print("parameter adpassword is not defined on configuration ")
		# 			sys.exit()
		if not d1['pod']['user']:
			d1['pod']['user']=user_env
		if vmmpassword_env:
			d1['pod']['vmmpassword'] = vmmpassword_env
		else:
			if 'vmmpassword' not in d1['pod']: 
				print("parameter vmmpassword is not defined on configuration ")
				sys.exit()
		#if not d1['']
		# add interface to vjunos_evolved VM
		#print(f"password AD {adpassword_env}, VMM {vmmpassword_env}")
		for i in d1['vm'].keys():
			if d1['vm'][i]['os']=='vjunos_evolved':
				## add interface em1, em2, em3, em4
				d1['vm'][i]['efi']='yes'
				# if 'vm_type' in d1['vm'][i].keys():
				# 	if d1['vm'][i]['vm_type'] == 0:
				# 		d1['vm'][i]['interfaces'].update({'vio1': {'mtu' : 9600, 'bridge' : i + 'PFE'}})
				# 		d1['vm'][i]['interfaces'].update({'vio2': {'mtu' : 9600, 'bridge' : i + 'RPIO'}})
				# 		d1['vm'][i]['interfaces'].update({'vio3': {'mtu' : 9600, 'bridge' : i + 'RPIO'}})
				# 		d1['vm'][i]['interfaces'].update({'vio4': {'mtu' : 9600, 'bridge' : i + 'PFE'}})
		# print("write tmp/lab.yaml")
		# with open('lab_new.yaml','w') as f1:
		#  	f1.write(yaml.dump(d1))

	except FileNotFoundError:
		print("where is the file")
	except PermissionError:
		print("Permission error")
	
	return(d1)

def change_loopback(d1):
	for i in d1['vm'].keys():
		if d1['vm'][i]['type'] in param1.vjunos_type:
			if 'lo0' in d1['vm'][i]['interfaces'].keys():
				if 'family' in d1['vm'][i]['interfaces']['lo0'].keys():
					if 'iso' in d1['vm'][i]['interfaces']['lo0']['family'].keys():
						d1['vm'][i]['interfaces']['lo0']['protocol']={'isis':'passive'}
def add_os(d1):
	list_of_os = set(d1['images'].keys())
	for i in d1['vm']:
		if 'os' not in d1['vm'][i].keys() and d1['vm'][i]['type'] in param1.pc_type_only:
			d1['vm'][i]['os']='ubuntu'
		elif 'os' not in d1['vm'][i].keys():
			d1['vm'][i]['os']=d1['vm'][i]['type']

		if d1['vm'][i]['os'] not in list_of_os:
			print(f"disk image {d1['vm'][i]['os']} is not defined in the configuration files (lab.yaml)")
			exit()

def change_ztp(d1):
	for i in d1['vm'].keys():
		if d1['vm'][i]['type'] in ['vjunos_switch','vjunos_router','vjunos_evolved','vjunos_evolvedBX','vsrx']:
			if 'ztp' not in d1['vm'][i].keys():
				d1['vm'][i]['ztp'] = True
			else:
				if type(d1['vm'][i]['ztp'])==int:
					if d1['vm'][i]['ztp'] <= 0:
						d1['vm'][i]['ztp'] = False
					else:
						d1['vm'][i]['ztp'] = True
			if 'mgmt_dhcp' not in d1['vm'][i].keys():
				d1['vm'][i]['mgmt_dhcp'] = False
			else:
				if type(d1['vm'][i]['mgmt_dhcp'])==int:
					if d1['vm'][i]['mgmt_dhcp'] <= 0:
						d1['vm'][i]['mgmt_dhcp'] = False
					else:
						d1['vm'][i]['mgmt_dhcp'] = True
			if 'mgmt_instc' not in d1['vm'][i].keys():
				d1['vm'][i]['mgmt_instc'] = True
			else:
				if type(d1['vm'][i]['mgmt_instc'])==int:
					if d1['vm'][i]['mgmt_instc'] <= 0:
						d1['vm'][i]['mgmt_instc'] = False
					else:
						d1['vm'][i]['mgmt_instc'] = True
			
				
def change_gateway4(d1):
	for i in d1['vm'].keys():
		if d1['vm'][i]['os'] in ['ubuntu','ubuntu2','desktop','debian']:
			for j in d1['vm'][i]['interfaces'].keys():
				#print(f"vm {i} interface {j}")
				if 'family' in d1['vm'][i]['interfaces'][j].keys():
					if 'inet' in d1['vm'][i]['interfaces'][j]['family'].keys():
						#print(f"host {i} {d1['vm'][i]['interfaces'][j]['family'].keys()}")
						#if 'gateway4' in d1['vm'][i]['interfaces'][j]['family']['inet'].keys():
						#if 'gateway4' in d1['vm'][i]['interfaces'][j].keys():
						if 'gateway4' in d1['vm'][i]['interfaces'][j]['family'].keys():
							#print("Create static")
							if 'static' in d1['vm'][i]['interfaces'][j]['family'].keys():
								#d1['vm'][i]['interfaces'][j]['static'].append({'to':'default','via':j['gateway4']})
								d1['vm'][i]['interfaces'][j]['family']['static'].append({'to':'0.0.0.0/0','via':d1['vm'][i]['interfaces'][j]['family']['gateway4']})
							else:
								#d1['vm'][i]['interfaces'][j]['static']=[{'to':'default','via': d1['vm'][i]['interfaces'][j]['gateway4']}]
								d1['vm'][i]['interfaces'][j]['family']['static']=[{'to':'0.0.0.0/0','via': d1['vm'][i]['interfaces'][j]['family']['gateway4']}]
							#d1['vm'][i]['interfaces'][j]['family'].pop('gateway4')
						else:
							print("no gateway4")
						if 'gateway6' in d1['vm'][i]['interfaces'][j]['family'].keys():
							if 'static' in d1['vm'][i]['interfaces'][j]['family'].keys():
								#d1['vm'][i]['interfaces'][j]['static'].append({'to':'default','via':j['gateway4']})
								d1['vm'][i]['interfaces'][j]['family']['static'].append({'to':'::/0','via':d1['vm'][i]['interfaces'][j]['family']['gateway6']})
							else:
								#d1['vm'][i]['interfaces'][j]['static']=[{'to':'default','via': d1['vm'][i]['interfaces'][j]['gateway4']}]
								d1['vm'][i]['interfaces'][j]['family']['static']=[{'to':'::/0','via': d1['vm'][i]['interfaces'][j]['family']['gateway6']}]
							#d1['vm'][i]['interfaces'][j]['family'].pop('gateway6')
		#print(d1['vm'][i])

def ipv4_to_int(ipv4):
	b1,b2,b3,b4 = ipv4.split('/')[0].split('.')
	retval = (int(b1) << 24) + (int(b2) << 16) + (int(b3) << 8) + int(b4)
	return retval

def create_config_interfaces(d1):
	num_link = len(d1['fabric']['topology'])
	for i in range(num_link):
		br='ptp' + str(i)
		d1['fabric']['topology'][i].append(br)
	#print("checkpoint 1")
	#num_link = num_link_with_ip(d1)
	if 'subnet' in d1['fabric']:
		# b1,b2,b3,b4 = d1['fabric']['subnet'].split('/')[0].split('.')
		# start_ip = (int(b1) << 24) + (int(b2) << 16) + (int(b3) << 8) + int(b4)
		start_ip=ipv4_to_int(d1['fabric']['subnet'])
		for i in range(num_link):
			if d1['fabric']['topology'][i][0]:
				if d1['fabric']['topology'][i][0] & param1.mask_ipv4:
					d1['fabric']['topology'][i].append(bin2ip(start_ip))
					start_ip += 1
					d1['fabric']['topology'][i].append(bin2ip(start_ip))
					start_ip += 1
				else:
					d1['fabric']['topology'][i].append('0')
					d1['fabric']['topology'][i].append('0')
	else:
		for i in range(num_link):
			if d1['fabric']['topology'][i]:
				d1['fabric']['topology'][i].append('0')
				d1['fabric']['topology'][i].append('0')
	if 'subnet6' in d1['fabric']:
		start_ip=0
		ipv6_address=d1['fabric']['subnet6'].split('/')[0]
		for i in range(num_link):
			if d1['fabric']['topology'][i][0]:
				if d1['fabric']['topology'][i][0] & param1.mask_ipv6:
					d1['fabric']['topology'][i].append(to_ipv6(ipv6_address,start_ip))
					start_ip += 1
					d1['fabric']['topology'][i].append(to_ipv6(ipv6_address,start_ip))
					start_ip += 1
				else:
					d1['fabric']['topology'][i].append('0')
					d1['fabric']['topology'][i].append('0')
	else:
		for i in range(num_link):
			if d1['fabric']['topology'][i]:
				if d1['fabric']['topology'][i][0] & param1.mask_ipv6:
					d1['fabric']['topology'][i].append('inet6')
					d1['fabric']['topology'][i].append('inet6')
				else:
					d1['fabric']['topology'][i].append('0')
					d1['fabric']['topology'][i].append('0')
		# print(d1['fabric'])
	# exit(1)
	list_vm = list_vm_from_fabric(d1)
	# print(d1['fabric']['topology'])
	# print(f"number of link {num_link}")
	# exit(1)
	#print(list_vm)
	d2={'vm': {} }
	for i in list_vm:
		d2['vm'].update({i : {'interfaces': {}}})
		for j in d1['fabric']['topology']:
			if j[1] == i:
				d2['vm'][i]['interfaces'].update( {j[2]: {'bridge' : j[5]} })
				if 'mtu' not in d2['vm'][i]['interfaces'][j[2]].keys():
					d2['vm'][i]['interfaces'][j[2]].update({'mtu' : param1.mtu  })
				else:
					d2['vm'][i]['interfaces'][j[2]]['mtu'] = param1.mtu
				if j[0] & param1.mask_iso:
					if 'family' not in d2['vm'][i]['interfaces'][j[2]].keys():
						d2['vm'][i]['interfaces'][j[2]].update({'family' : {'iso':None}})
					else:
						d2['vm'][i]['interfaces'][j[2]]['family'].update({'iso':None})
					if j[0] & param1.mask_isis:
						if 'protocol' not in d2['vm'][i]['interfaces'][j[2]].keys():
							d2['vm'][i]['interfaces'][j[2]].update({'protocol' : {'isis':'ptp'}})
						else:
							d2['vm'][i]['interfaces'][j[2]]['protocol'].update({'isis':'ptp'})
				if j[0] & param1.mask_ipv6:
					if 'family' not in d2['vm'][i]['interfaces'][j[2]].keys():
						d2['vm'][i]['interfaces'][j[2]].update({'family' : {'inet6': j[8]}})
					else:
						d2['vm'][i]['interfaces'][j[2]]['family'].update({'inet6': j[8]})
						
				if j[0] & param1.mask_ipv4:
					if 'family' not in d2['vm'][i]['interfaces'][j[2]].keys():
						d2['vm'][i]['interfaces'][j[2]].update({'family' : {'inet': j[6]}})
					else:
						d2['vm'][i]['interfaces'][j[2]]['family'].update({'inet': j[6]})
					
					if j[0] & param1.mask_mpls:
						if 'family' not in d2['vm'][i]['interfaces'][j[2]].keys():
							d2['vm'][i]['interfaces'][j[2]].update({'family' : {'mpls':None}})
						else:
							d2['vm'][i]['interfaces'][j[2]]['family'].update({'mpls':None})
						if j[0] & param1.mask_rsvp:
							if 'protocol' not in d2['vm'][i]['interfaces'][j[2]].keys():
								d2['vm'][i]['interfaces'][j[2]].update({'protocol' : {'rsvp':None}})
							else:
								d2['vm'][i]['interfaces'][j[2]]['protocol'].update({'rsvp':None})
						if j[0] & param1.mask_ldp:
							if 'protocol' not in d2['vm'][i]['interfaces'][j[2]].keys():
								d2['vm'][i]['interfaces'][j[2]].update({'protocol' : {'ldp':None}})
							else:
								d2['vm'][i]['interfaces'][j[2]]['protocol'].update({'ldp':None})
					if j[0] & param1.mask_rpm:
						src = d2['vm'][i]['interfaces'][j[2]]['family']['inet'].split('/')[0]
						dst = calc_target(src)
						if 'rpm' not in d2['vm'][i]['interfaces'][j[2]].keys():
							d2['vm'][i]['interfaces'][j[2]].update({'rpm' : {'source': src, 'destination': dst } })
						else:
							d2['vm'][i]['interfaces'][j[2]]['rpm'] = {'source': src, 'destination': dst }
				# if j[0] & param1.mtu:
				# 	if 'mtu' not in d2['vm'][i]['interfaces'][j[2]].keys():
				# 		d2['vm'][i]['interfaces'][j[2]].update({'mtu' : param1.mtu  })
				# 	else:
				# 		d2['vm'][i]['interfaces'][j[2]]['mtu'] = param1.mtu

				intf_desc = j[4].replace("em","eth") if "em" in j[4] else j[4]
				#print(intf_desc)
				d2['vm'][i]['interfaces'][j[2]]['desc']= f"connection to port {intf_desc} of {j[3]}"
				#print(d2)

			elif j[3] == i:
				d2['vm'][i]['interfaces'].update({j[4]: {'bridge' : j[5]} })
				if 'mtu' not in d2['vm'][i]['interfaces'][j[4]].keys():
					d2['vm'][i]['interfaces'][j[4]].update({'mtu' : param1.mtu  })
				else:
					d2['vm'][i]['interfaces'][j[4]]['mtu'] = param1.mtu
				if j[0] & param1.mask_iso:
					if 'family' not in d2['vm'][i]['interfaces'][j[4]].keys():
						d2['vm'][i]['interfaces'][j[4]].update({'family' : {'iso':None}})
					else:
						d2['vm'][i]['interfaces'][j[4]]['family'].update({'iso':None})
					if j[0] & param1.mask_isis:
						if 'protocol' not in d2['vm'][i]['interfaces'][j[4]].keys():
							d2['vm'][i]['interfaces'][j[4]].update({'protocol' : {'isis':'ptp'}})
						else:
							d2['vm'][i]['interfaces'][j[4]]['protocol'].update({'isis':'ptp'})
				if j[0] & param1.mask_ipv6:
					if 'family' not in d2['vm'][i]['interfaces'][j[4]].keys():
						d2['vm'][i]['interfaces'][j[4]].update({'family' : {'inet6': j[9]}})
					else:
						d2['vm'][i]['interfaces'][j[4]]['family'].update({'inet6': j[9]})
				if j[0] & param1.mask_ipv4:
					if 'family' not in d2['vm'][i]['interfaces'][j[4]].keys():
						d2['vm'][i]['interfaces'][j[4]].update({'family' : {'inet': j[7]}})
					else:
						d2['vm'][i]['interfaces'][j[4]]['family'].update({'inet': j[7]})
					
					if j[0] & param1.mask_mpls:
						if 'family' not in d2['vm'][i]['interfaces'][j[4]].keys():
							d2['vm'][i]['interfaces'][j[4]].update({'family' : {'mpls':None}})
						else:
							d2['vm'][i]['interfaces'][j[4]]['family'].update({'mpls':None})
					
						if j[0] & param1.mask_rsvp:
							if 'protocol' not in d2['vm'][i]['interfaces'][j[4]].keys():
								d2['vm'][i]['interfaces'][j[4]].update({'protocol' : {'rsvp':None}})
							else:
								d2['vm'][i]['interfaces'][j[4]]['protocol'].update({'rsvp':None})
						if j[0] & param1.mask_ldp:
							if 'protocol' not in d2['vm'][i]['interfaces'][j[4]].keys():
								d2['vm'][i]['interfaces'][j[4]].update({'protocol' : {'ldp':None}})
							else:
								d2['vm'][i]['interfaces'][j[4]]['protocol'].update({'ldp':None})
					if j[0] & param1.mask_rpm:
						src = d2['vm'][i]['interfaces'][j[4]]['family']['inet'].split('/')[0]
						dst = calc_target(src)
						if 'rpm' not in d2['vm'][i]['interfaces'][j[4]].keys():
							d2['vm'][i]['interfaces'][j[4]].update({'rpm' : {'source': src, 'destination': dst } })
						else:
							d2['vm'][i]['interfaces'][j[4]]['rpm'] = {'source': src, 'destination': dst }

				intf_desc = j[2].replace("em","eth") if "em" in j[2] else j[2]
				d2['vm'][i]['interfaces'][j[4]]['desc']= f"connection to port {intf_desc} of {j[1]}"
				# if j[0] & param1.mtu:
				# 	if 'mtu' not in d2['vm'][i]['interfaces'][j[4]].keys():
				# 		d2['vm'][i]['interfaces'][j[4]].update({'mtu' : param1.mtu  })
				# 	else:
				# 		d2['vm'][i]['interfaces'][j[4]]['mtu'] = param1.mtu

	for i in d2['vm'].keys():
		intf = d2['vm'][i]['interfaces']
		#pprint.pprint(intf)
		d1['vm'][i]['interfaces'].update(intf)	
	#print(d2)
	for i in d1['vm'].keys():
		# print(f"vm {i}")
		if d1['vm'][i]['type']=='bridge':
			list_intf=list(d1['vm'][i]['interfaces'].keys())
			#print(f"list of intf {list_intf}")
			#print(list_intf)
			_ = list_intf.pop(0)
			#print(list_intf)
			#print(f"list_intf {list_intf}")
			for j in list_intf:
				node_tmp1 = d1['vm'][i]['interfaces'][j]['node']
				#print(f"node_tmp1 {node_tmp1}")
				#print(node_tmp1)
				n1 = d1['vm'][i]['interfaces'][j]['node'][0]
				n1_intf = d1['vm'][i]['interfaces'][j]['node'][1]
				d1['vm'][i]['interfaces'][j] = {'bridge' : i + j}
				#print(f"node {i} {j} {n1} {n1_intf}")
				#print(d1['vm'][n1]['interfaces'].keys())
				d1['vm'][n1]['interfaces'][n1_intf]['bridge']=d1['vm'][i]['interfaces'][j]['bridge']
				d1['vm'][i]['interfaces'][j]['node'] = node_tmp1
	d1.pop('fabric')


def calc_target(src_ip):
	ip_byte = src_ip.split('.')
	if int(ip_byte[3]) % 2:
		ip_byte[3]=str(int(ip_byte[3])-1)
	else:
		ip_byte[3]=str(int(ip_byte[3])+1)
	return '.'.join(ip_byte)

def list_vm_from_fabric(d1):
	junos_vm_f1= []
	for i in d1['fabric']['topology']:
		if i[1] not in junos_vm_f1:
			junos_vm_f1.append(i[1])
		if i[3] not in junos_vm_f1:
			junos_vm_f1.append(i[3])
	return junos_vm_f1

def bin2ip(ipbin):
	m1 = 255<<24
	m2 = 255<<16
	m3 = 255 << 8
	m4 = 255
	b1=str((ipbin & m1) >> 24)
	b2=str((ipbin & m2) >> 16)
	b3=str((ipbin & m3) >> 8)
	b4=str(ipbin & m4)
	retval = '.'.join((b1,b2,b3,b4)) + "/31"
	#print(retval)
	return retval

def to_ipv6(ipv6_address,last_number):
	ipv6_list=ipv6_address.split(":")
	while("" in ipv6_list):
		ipv6_list.remove("")
	t1 = str(hex(last_number)).split('x')[1]
	retval = ':'.join(ipv6_list) + "::" + t1 + "/127"

	return retval


def check_ip(d1):
	preflen = 32 - int(d1['fabric']['subnet'].split('/')[1])
	mask_ip = int(2** preflen - 1) 
	b1,b2,b3,b4 = d1['fabric']['subnet'].split('/')[0].split('.')
	ip_int = (int(b1) << 24) + (int(b2) << 16) + (int(b3) << 8) + int(b4)
	#print("ip int : ",bin(ip_int))
	#print("mask   : ",bin(mask_ip))
	retval = ip_int & mask_ip
	#print("retval = ",retval)
	return retval

def check_vm(d1):
	junos_vm_d1 = []
	for i in d1['vm'].keys():
		if d1['vm'][i]['type'] in ['junos','veos']:
			if i not in junos_vm_d1:
				junos_vm_d1.append(i)
	junos_vm_f1= list_vm_from_fabric(d1)
	return set(junos_vm_f1).issubset(set(junos_vm_d1))

# old function
# def add_ssh_key(d1):
# 	if 'ssh_key_name' in d1['pod'].keys():
# 		key_file = str(pathlib.Path.home()) + "/.ssh/" + d1['pod']['ssh_key_name'] + ".pub"
# 		key_file_priv = str(pathlib.Path.home()) + "/.ssh/" + d1['pod']['ssh_key_name']
# 	else:
# 		key_file = str(pathlib.Path.home()) + "/.ssh/id_rsa.pub"
# 		key_file_priv = str(pathlib.Path.home()) + "/.ssh/id_rsa"
# 	try:
# 		with open(key_file) as f:
# 			ssh_key = f.read()
# 		d1['pod']['ssh_key']=ssh_key.strip()
# 		with open(key_file_priv) as f:
# 			ssh_key_priv = f.read()
# 		d1['pod']['ssh_key_priv']=ssh_key_priv.strip()
# 		if 'ssh_key_host_name' in d1['pod'].keys():
# 			key_file = str(pathlib.Path.home()) + "/.ssh/" + d1['pod']['ssh_key_host_name'] + ".pub"
# 			key_file_priv = str(pathlib.Path.home()) + "/.ssh/" + d1['pod']['ssh_key_host_name']
# 			with open(key_file) as f:
# 				ssh_key = f.read()
# 			d1['pod']['ssh_key_host']=ssh_key.strip()
# 			with open(key_file_priv) as f:
# 				ssh_key_priv = f.read()
# 			d1['pod']['ssh_key_host_priv']=ssh_key_priv.strip()
# 		else:
# 			d1['pod']['ssh_key_host']=d1['pod']['ssh_key']
# 			d1['pod']['ssh_key_host_priv']=d1['pod']['ssh_key_priv']
# 	except Exception as e:
# 		print(e)
# 		sys.exit()


# create ssh key
def create_ssh_key(d1):
	# Generate an RSA private key
	ssh_dir = os.path.expanduser('~')  + "/.ssh/"
	ssh_key_priv_file = ssh_dir + d1['name']
	ssh_key_pub_file = ssh_dir + d1['name'] + ".pub"
	# check file existence
	key_file_not_avail = 1
	if os.path.isfile(ssh_key_priv_file) and os.path.isfile(ssh_key_pub_file):
		key_file_not_avail = 0

	if key_file_not_avail:
		rsa_private_key = rsa.generate_private_key(
			public_exponent=65537,
			key_size=2048,
			backend=default_backend()
		)

		# Serialize the RSA private key to OpenSSH format
		pem_private_key = rsa_private_key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.OpenSSH,
			encryption_algorithm=serialization.NoEncryption() # Use NoEncryption or a password
		)

		# Get the public key in OpenSSH format
		ssh_public_key = rsa_private_key.public_key().public_bytes(
			encoding=serialization.Encoding.OpenSSH,
			format=serialization.PublicFormat.OpenSSH
		)

		# Save to files
		with open(ssh_key_priv_file, "wb") as f:
			f.write(pem_private_key)
		os.chmod(ssh_key_priv_file,0o600)
		with open(ssh_key_pub_file, "wb") as f:
			f.write(ssh_public_key)
# revised function
def add_ssh_key(d1):
	# if 'ssh_key_name' in d1['pod'].keys():
	# 	key_file = str(pathlib.Path.home()) + "/.ssh/" + d1['pod']['ssh_key_name'] + ".pub"
	# 	key_file_priv = str(pathlib.Path.home()) + "/.ssh/" + d1['pod']['ssh_key_name']
	# else:
	# 	key_file = str(pathlib.Path.home()) + "/.ssh/id_rsa.pub"
	# 	key_file_priv = str(pathlib.Path.home()) + "/.ssh/id_rsa"
	create_ssh_key(d1)
	ssh_dir = os.path.expanduser('~')  + "/.ssh/"
	key_file_priv = ssh_dir + d1['name']
	key_file  = ssh_dir + d1['name'] + ".pub"
	with open(key_file) as f:
		ssh_key = f.read()
	d1['pod']['ssh_key_host']=ssh_key.strip()
	with open(key_file_priv) as f:
		ssh_key_priv = f.read()
	d1['pod']['ssh_key_host_priv']=ssh_key_priv.strip()

def add_path(d1,path):
	d1['pod']['path']=path
	d1['template']={
		'junos': f"{path}/template/junos.j2",
		'junos1': f"{path}/template/junos.j2",
		'junos2': f"{path}/template/junos2.j2",
		'junos3': f"{path}/template/junos3.j2",
		'set_gw': f"{path}/template/set_gw.j2",
		'set_gw2': f"{path}/template/set_gw2.j2",
		'kea_dhcp4': f"{path}/template/kea_dhcp4.j2",
		'ztp_dhcp': f"{path}/template/ztp_dhcp.j2",
		'dhcp': f"{path}/template/dhcp.j2",
		'vjunos_config': f"{path}/template/vjunos_config.j2",
		'ubuntu': f"{path}/template/ubuntu.j2",
		'debian': f"{path}/template/debian.j2",
		'centos': f"{path}/template/centos.j2",
		'bridge': f"{path}/template/bridge.j2",
		'vmmtopo': f"{path}/template/vmm_topology.j2",
		'ssh_config': f"{path}/template/ssh_config.j2"
	}

# def get_private_ip_gw(d1):
# 	for i in d1['vm'].keys():
# 		if d1['vm'][i]['type']=="gw":
# 			for j in d1['vm'][i]['interfaces'].keys():
# 				if d1['vm'][i]['interfaces'][j]['bridge']=="mgmt":
# 					retval= d1['vm'][i]['interfaces'][j]['family']['inet'].split("/")[0]
# 	return retval

def print_syntax():
	print("usage : vmm.py <command>")
	print("commands are : ")
	print("  upload : to upload configuration to vmm pod ")
	print("  start  : to start VM in the vmm pod")
	print("  stop   : to stop in the vmm pod")
	print("  list   : list of running VM")
	#print("  get_serial : get serial information of the vm")
	#print("  get_vga : get vga information of the vm (for vnc)")
	#print("  get_ip  : get IP information of the vm")
	print("  set_gw  : setting gateway configuration")
	print("  set_host  : setting ubuntu/centos configuration")
	print("  init_junos  : initial configuration for vEX and vEVO")
	print("  config_junos  : push configuration for vEX and vEVO")
	print("if configuration file is not specified, then file lab.yaml must be present")

def check_argv(argv):
	retval={}
	cmd_list=['upload','start','stop','get_serial','get_vga','get_ip','list','config','test','init_junos','config_junos','change_dhcp','check_vmm_capacity']
	if len(argv) == 1:
		print_syntax()
	else:
		if not os.path.isfile("./lab.yaml"):
			print("file lab.conf doesn't exist, please create one or define another file for configuration")
		else:
			retval['config_file']="lab.yaml"
			retval['cmd']=argv[1]
			t1 = argv[0].split("/")
			_ = t1.pop()
			path = '/'.join(t1)
			# retval['template']={
			# 	'junos': f"{path}/template/junos.j2",
			# 	'set_gw': f"{path}/template/set_gw.j2"
			# }
			# path=""
			# for i in list(range(2)):
			# 	path += t1[i] + "/"
			#print("path ",path)
			retval['path']=path
			if retval['cmd'] == 'get_ip':
				if len(argv)==2:
					print("get_ip requires VM information")
					retval={}
				elif len(argv)==3:
					retval['vm'] = argv[2]
			elif retval['cmd'] == 'get_vga': 
				if len(argv)==3:
					retval['vm'] = argv[2]
				else:
					retval['vm'] = ""
			elif retval['cmd'] == 'get_serial': 
				if len(argv)==3:
					retval['vm'] = argv[2]
				else:
					retval['vm'] = ""
			elif retval['cmd'] == 'init_junos': 
				#print(f"len {len(argv)}")
				if len(argv)==3:
					retval['vm'] = argv[2]
				else:
					retval['vm']= False
			elif retval['cmd'] == 'set_host': 
				#print(f"len {len(argv)}")
				if len(argv)==3:
					retval['vm'] = argv[2]
				else:
					retval['vm']= ""

	return retval

def checking_config_syntax(d1):
	retval=1
	# checking type and os
	for i in d1['vm'].keys():
		# checking vm type
		if not d1['vm'][i]['type'] in param1.vm_type.keys():
			print("ERROR for VM ",i)
			print("this type of VM, " + d1['vm'][i]['type'] + " is not supported yet")
			return 0
		#print("param1.vm_os",param1.vm_os)
		# if not d1['vm'][i]['os'] in param1.vm_os:
		# 	print("ERROR for VM ",i)
		# 	print("this OS " + d1['vm'][i]['os'] + " is not supported yet")
		# 	return 0
	# checking interface
	for i in d1['vm'].keys():
		if (d1['vm'][i]['type'] in param1.vm_type.keys()) and (d1['vm'][i]['type'] not in ['vmx','vjunos_evolved','vjunos_evolvedBX','vsrx','mx240','mx480','mx960','vjunos_switch','vjunos_router']):
			for j in d1['vm'][i]['interfaces'].keys():
				if 'em' not in j:
					print("ERROR for VM ",i)
					print("interface " + j + " is not supported")
					return 0
			for j in d1['vm'][i]['interfaces'].keys():
				if list(d1['vm'][i]['interfaces'].keys()).count(j) > 1:
					print("ERROR for VM ",i)
					print("duplicate interfaces " + j + " is found")
					return 0
	return retval

# def get_ip(d1,vm):
# 	if d1['pod']['type'] == 'vmm':
# 		ssh=ƒ(d1)
# 		#print('-----')
# 		#print(" of VM")
# 		cmd1="vmm list"
# 		s1,s2,s3=ssh.exec_command(cmd1)
# 		vm_list=[]
# 		for i in s2.readlines():
# 			vm_list.append(i.rstrip().split()[0])
# 		if vm not in vm_list:
# 			print(" VM {} does not exists ".format(vm))	
# 		else:
# 			print("VM %s %s " %(vm,get_ip_vm(d1,vm)))
# 		ssh.close()
# 	elif d1['pod']['type'] == 'kvm':
# 		print("not yet implemented")



def sshconnect(d1):
	# if 'jumpserver' in d1['pod'].keys():
	# 	jumphost=paramiko.SSHClient()
	# 	jumphost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# 	jumphost.connect(hostname=d1['pod']['jumpserver'],username=d1['pod']['user'],password=d1['pod']['adpassword'])
	# 	jumphost_transport=jumphost.get_transport()
	# 	src_addr=(d1['pod']['jumpserver'],22)
	# 	dest_addr=(d1['pod']['vmmserver'],22)
	# 	jumphost_channel = jumphost_transport.open_channel("direct-tcpip", dest_addr, src_addr)
	# 	ssh=paramiko.SSHClient()
	# 	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# 	# ssh.connect(hostname=d1['pod']['vmmserver'],username=d1['pod']['user'],password=d1['pod']['unixpassword'],sock=jumphost_channel)
	# 	ssh.connect(hostname=d1['pod']['vmmserver'],username=d1['pod']['user'],password=d1['pod']['vmmpassword'],sock=jumphost_channel)
	# else:
	# 	ssh=paramiko.SSHClient()
	# 	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# 	ssh.connect(hostname=d1['pod']['vmmserver'],username=d1['pod']['user'],password=d1['pod']['vmmpassword'])
	# return ssh
	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=d1['pod']['vmmserver'],username=d1['pod']['user'],password=d1['pod']['vmmpassword'])
	return ssh
	# ssh=paramiko.SSHClient()
	# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# #print(f"User {d1['pod']['user']}, password {d1['pod']['vmmpassword']}")
	# ssh.connect(hostname=d1['pod']['vmmserver'],username=d1['pod']['user'],password=d1['pod']['vmmpassword'])
	# return ssh

def connect_to_gw(d1):
	if not 'gw_ip' in d1.keys():
		d1['gw_ip'] = get_ip_vm(d1,'gw')
	user_id = get_ssh_user(d1,'gw')
	passwd='pass01'
	if 'jumpserver' in d1['pod'].keys():
		# jumphost=paramiko.SSHClient()
		# jumphost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# jumphost.connect(hostname=d1['pod']['jumpserver'],username=d1['pod']['user'],password=d1['pod']['adpassword'])
		# jumphost_transport=jumphost.get_transport()
		# src_addr=(d1['pod']['jumpserver'],22)
		# dest_addr=(d1['gw_ip'],22)
		# jumphost_channel = jumphost_transport.open_channel("direct-tcpip", dest_addr, src_addr)
		# ssh=paramiko.SSHClient()
		# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# # ssh.connect(hostname=d1['pod']['vmmserver'],username=d1['pod']['user'],password=d1['pod']['unixpassword'],sock=jumphost_channel)
		# ssh.connect(hostname=d1['gw_ip'],username=user_id,password=passwd,sock=jumphost_channel)

		jumphost=paramiko.SSHClient()
		jumphost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		#jumphost.connect(hostname=d1['pod']['jumpserver'],username=d1['pod']['user'],password=d1['pod']['adpassword'])
		jumphost.connect(hostname=d1['pod']['vmmserver'],username=d1['pod']['user'],password=d1['pod']['vmmpassword'])
		jumphost_transport=jumphost.get_transport()
		src_addr=(d1['pod']['vmmserver'],22)
		dest_addr=(d1['gw_ip'],22)
		jumphost_channel = jumphost_transport.open_channel("direct-tcpip", dest_addr, src_addr)
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# ssh.connect(hostname=d1['pod']['vmmserver'],username=d1['pod']['user'],password=d1['pod']['unixpassword'],sock=jumphost_channel)
		ssh.connect(hostname=d1['gw_ip'],username=user_id,password=passwd,sock=jumphost_channel)
	else:
		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=d1['gw_ip'],username=user_id,password=passwd)
	return ssh
	# ssh=paramiko.SSHClient()
	# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# ssh.connect(hostname=d1['gw_ip'],username=user_id,password=passwd)
	# return ssh

def get_mgmt_ip(d1,i):
	print(f"type {d1['vm'][i]['type']} ")
	if d1['vm'][i]['type'] in ['junos','vjunos_router','vjunos_switch']:
		ip_vm = d1['vm'][i]['interfaces']['mgmt']['family']['inet'].split('/')[0]
	else:
		ip_vm = d1['vm'][i]['interfaces']['em0']['family']['inet'].split('/')[0]
	return ip_vm

def get_user(d1,i):
	if d1['vm'][i]['type']=='junos':
		user_id = d1['junos_login']['login']
		passwd = d1['junos_login']['password']
	elif d1['vm'][i]['os'] in ['ubuntu','ubuntu2']:
		user_id = 'ubuntu'
		passwd = 'pass01'
	elif d1['vm'][i]['os']=='desktop':
		user_id = 'ubuntu'
		passwd = 'pass01'
	elif d1['vm'][i]['os']=='centos':
		user_id = 'centos'
		passwd = 'pass01'
	elif d1['vm'][i]['os']=='rhel':
		user_id = 'rhel'
		passwd = 'pass01'
	elif d1['vm'][i]['os']=='debian':
		user_id = 'debian'
		passwd = 'pass01'
	elif d1['vm'][i]['os']=='alpine':
		user_id = 'alpine'
		passwd = 'pass01'
	elif d1['vm'][i]['os']=='bridge':
		user_id = 'alpine'
		passwd = 'pass01'
	else:
		user_id = 'admin'
		passwd = 'pass01'

	return user_id,passwd

def get_vga(d1,vm=""):
	if d1['pod']['type'] == 'vmm':
		print("get_vga , vm ",vm)
		print('-----')
		ssh=sshconnect(d1)
		cmd1="vmm list"
		s1,s2,s3=ssh.exec_command(cmd1)
		vm_list=[]
		for i in s2.readlines():
			vm_list.append(i.rstrip().split()[0])	
		ssh.close()
		if vm != "":
			if vm not in vm_list:
				print("VM %s does not exist " %(vm))
			else:
				print_vga(d1,vm)
		else:
			for i in vm_list:
				print_vga(d1,i)
	elif d1['pod']['type'] == 'kvm':
		print("not yet implemented")
			

def get_vncinfo(d1,vm):
	ssh=sshconnect(d1)
	cmd1=f"vmm args {vm} | grep \"vnc\""
	s1,s2,s3=ssh.exec_command(cmd1)
	#print("host ",vm)
	vnc_server = "VGA port is disabled "
	for j in s2.readlines():
		if j.strip().split()[1] == 'none':
			vnc_server = "VGA port is disabled "
		else:
			vnc_server =  j.strip().split()[1]
			# vnc_port = int(j.rstrip().split()[1].split(':')[1]) + 5900 
	ssh.close()
	return vnc_server

def get_vnc_list(d1):
	ssh=sshconnect(d1)
	vm_with_vnc=[]
	retval = None
	for i in d1['vm'].keys():		
		if 'vnc' in d1['vm'][i].keys():
			if d1['vm'][i]['vnc']:
				vm_with_vnc.append(i)
	cmd_list=[]
	for i in vm_with_vnc:
		cmd_list.append(f"vmm args {i} | grep \"vnc\"")
	cmd = ";".join(cmd_list)
	print(f"list of vm with vnc enabled {vm_with_vnc}")
	#print(cmd)
	_,s2,_=ssh.exec_command(cmd)
	vnc_server=[]
	for j in s2.readlines():
		t1 =  j.strip().split()[1]
		vnc_server.append(t1)
	retval = dict(zip(vm_with_vnc,vnc_server))
	d1=yaml.dump(retval)
	print(d1)
	return retval

def print_vga(d1,vm):
	print("VGA port of " + vm + " -> " + get_vncinfo(d1,vm))


def get_ip_vm(d1,i):
	if d1['pod']['type'] == 'vmm':
		ssh=sshconnect(d1)
		cmd1="vmm args " + i + " | grep \" ip \""
		# xxx=''''''
		stdin,stdout,sstderr=ssh.exec_command(cmd1)
		j = stdout.readlines()
		ssh.close()
		_,retval= j[0].rstrip().split()
		if retval == 'None':
			retval = "No External IP"
		return retval
	elif d1['pod']['type'] == 'kvm':
		print("not implemented for this type")
		return ""

# def get_hosts_config(d1):
# 	host_yes=['centos','rhel','ubuntu','ubuntu2','debian','esxi','aos','aos_ztp','bridge','desktop']
# 	host_config=['127.0.0.1 localhost','::1 ip6-localhost ip6-loopback']
# 	for i in d1['vm'].keys():
# 		if d1['vm'][i]['os'] in host_yes:
# 			for j in d1['vm'][i]['interfaces'].keys():
# 				#print(f"HOST {i}, Interfaces {j}")
# 				if 'family' in d1['vm'][i]['interfaces'][j].keys():
# 					if 'inet' in d1['vm'][i]['interfaces'][j]['family'].keys():
# 						ipaddr=d1['vm'][i]['interfaces'][j]['family']['inet'].split('/')[0]
# 						host_config.append("{} {}".format(ipaddr,i))
# 	return host_config


def get_dhcp_config(d1):
	#dhcp_yes=['centos','rhel','ubuntu','ubuntu2','debian','esxi','bridge','desktop','paagent','vjunos_switch','vjunos_router','vjunos_evolved','vjunos_evolvedBX','aos','aos_flow','aos_ztp']
	dhcp_list=[]
	retval={}
	t1={}
	print("Getting dhcp config")
	for i in d1['vm'].keys():
		# if d1['vm'][i]['os'] in dhcp_yes:
		#print(f"checking {i}")
		if 'em0' in d1['vm'][i]['interfaces']:
			if 'family' in d1['vm'][i]['interfaces']['em0']:
				if 'inet' in d1['vm'][i]['interfaces']['em0']['family']:
					d1['vm'][i]['interfaces']['em0']['mac']=get_mac_vm(d1,i)
					print(f"vm {i} mac {d1['vm'][i]['interfaces']['em0']['mac']}")
					dhcp_list.append(i)
		elif 'mgmt' in d1['vm'][i]['interfaces']:
			if d1['vm'][i]['type'] in ['vjunos_switch','vjunos_router','vjunos_evolved','vjunos_evolvedBX'] and d1['vm'][i]['ztp']:
				if 'family' in d1['vm'][i]['interfaces']['mgmt']:
					if 'inet' in d1['vm'][i]['interfaces']['mgmt']['family']:
						d1['vm'][i]['interfaces']['mgmt']['mac']=get_mac_vm(d1,i)
						dhcp_list.append(i)
	#print(f"list of vm with dhcp {dhcp_list}")
	#print("get_dhcp_config")
	for i in dhcp_list:
		if 'mgmt' in d1['vm'][i]['interfaces'].keys(): 
			t1[i]={
				'ip' : d1['vm'][i]['interfaces']['mgmt']['family']['inet'].split('/')[0],
				'mac' : d1['vm'][i]['interfaces']['mgmt']['mac'],
				'type' : 'junos'
			}
		elif 'em0' in d1['vm'][i]['interfaces'].keys(): 
			t1[i]={
				'ip' : d1['vm'][i]['interfaces']['em0']['family']['inet'].split('/')[0],
				'mac' : d1['vm'][i]['interfaces']['em0']['mac'],
				'type' : 'pc'
			}
		print(f"vm {i}, ip {t1[i]['ip']}, mac {t1[i]['mac']}")
	
	retval['dhcp']={
		'vm': t1
	}
	# cmd1 = "systemd-resolve --status | grep -A1 -m 1 \"DNS Servers\" | sed -e 's/DNS Servers://' | sed -e 's/ *//'"
	# ssh=sshconnect(d1)
	# _,stdout,_=ssh.exec_command(cmd1)
	# j = stdout.readlines()
	# #print(f"output {j}")
	# retval['dhcp']['dns']=[]
	# for i in j:
	# 	#print(i)
	# 	#print(i)
	# 	t1= i.rstrip()
	# 	#print(t1)
	# 	retval['dhcp']['dns'].append(t1)
	retval['dhcp']['dns']=param1.jnpr_dns
	retval['dhcp']['range']=[]

	#print(f"retval {retval}")
	intf_list = []
	id = 1
	for i in d1['vm']['gw']['interfaces'].keys():
		if 'dhcp_range' in d1['vm']['gw']['interfaces'][i].keys():
			low_ip,high_ip = d1['vm']['gw']['interfaces'][i]['dhcp_range'].split('-')
			ip_subnet, subnet_mask = get_subnet(d1['vm']['gw']['interfaces'][i]['family']['inet'])
			intf_list.append(i.replace('em','eth'))
			retval['dhcp']['range'].append({
				'min': low_ip,
				'max': high_ip,
				'router': d1['vm']['gw']['interfaces'][i]['family']['inet'].split('/')[0],
				'subnet' : ip_subnet,
				'prefix' : netmask2prefix(subnet_mask),
				'netmask' : subnet_mask,
				'id' : id
			})
			id+=1
	retval['dhcp']['intf'] = intf_list
	retval['net'] = get_net_config_gw(d1)
	retval['vnc'] = create_novnc(d1)
	# cmd1 = "ip addr show dev eth0 | grep 'inet ' | tr -s ' ' | cut -f 3 -d ' ' | cut -f 1 -d '/'"
	# ssh=sshconnect(d1)
	# _,stdout,_=ssh.exec_command(cmd1)
	# j = stdout.readlines()
	#print(f"value of j {j}")
	#retval['ip_gw'] = d1['vm']['gw']['interfaces']['em1']['family']['inet'].split('/')[0]
	retval['ip_gw'] = get_ip_vm(d1,'gw')
	retval['ssh_key_pub'] = d1['pod']['ssh_key_host']
	retval['ssh_key_priv'] = d1['pod']['ssh_key_host_priv']

	#print(retval)
	#print(retval.keys())
	#print(retval['vnc'])
	return retval


def get_net_config(d1,vm):
	print("get net config ",vm)
	net_config={}
	static_config={}
	mtu_config={}
	retval = {}
	addr={}
	prefix={}
	bridge={}
	for i in d1['vm'][vm]['interfaces'].keys():
		j = i.replace('em','eth')
		retval[j]={
			'addresses': None,
			'addr' : None,
			'prefix': None,
			'static': None,
			'mtu': None,
			'dns': None,
			'gateway4': None,
			'gateway6': None,
			'search' : 'vmmlab.com'
		}

	for i in d1['vm'][vm]['interfaces'].keys():
		j = i.replace('em','eth')
		if 'family' in d1['vm'][vm]['interfaces'][i].keys():
			if j not in net_config.keys():
				net_config[j]=[]
				addr[j]=[]
				prefix[j]=[]
			if 'inet' in d1['vm'][vm]['interfaces'][i]['family'].keys():
				net_config[j].append(d1['vm'][vm]['interfaces'][i]['family']['inet'])
				addr[j].append(d1['vm'][vm]['interfaces'][i]['family']['inet'].split('/')[0])
				prefix[j].append(d1['vm'][vm]['interfaces'][i]['family']['inet'].split('/')[1])
				if 'gateway4' in d1['vm'][vm]['interfaces'][i]['family'].keys():
					retval[j]['gateway4'] = d1['vm'][vm]['interfaces'][i]['family']['gateway4']
			if 'inet6' in d1['vm'][vm]['interfaces'][i]['family'].keys():
				if d1['vm'][vm]['interfaces'][i]['family']['inet6'] != "inet6":
					net_config[j].append(d1['vm'][vm]['interfaces'][i]['family']['inet6'])
					addr[j].append(d1['vm'][vm]['interfaces'][i]['family']['inet6'].split('/')[0])
					prefix[j].append(d1['vm'][vm]['interfaces'][i]['family']['inet6'].split('/')[1])
					if 'gateway6' in d1['vm'][vm]['interfaces'][i]['family'].keys():
						retval[j]['gateway6'] = d1['vm'][vm]['interfaces'][i]['family']['gateway6']
			if 'static' in d1['vm'][vm]['interfaces'][i]['family'].keys():
				static_config[j]=d1['vm'][vm]['interfaces'][i]['family']['static']
		if 'mtu' in d1['vm'][vm]['interfaces'][i].keys():
			mtu_config[j]=d1['vm'][vm]['interfaces'][i]['mtu']
	for i in d1['vm'][vm]['interfaces'].keys():
		j = i.replace('em','eth')
		if 'node' in d1['vm'][vm]['interfaces'][i].keys():
			br_name =  d1['vm'][vm]['interfaces'][i]['node'][2]
			if bridge:
				if br_name not in bridge.keys():
					bridge[br_name]=[j]
				else:
					bridge[br_name].append(j)
			else:
				bridge={br_name : [j]}
	# for j in bridge.keys():
	# 	br_temp = " ".join(bridge[j])
		# bridge[j] = br_temp
	for j in retval.keys():
		if j in net_config.keys():
			retval[j]['addresses']=net_config[j]
			if j == 'eth0':
				# retval[j]['dns']=d1['pod']['dns']
				retval[j]['dns']=retval[j]['gateway4']
		if j in static_config.keys():
			retval[j]['static'] =  static_config[j]
		if j in mtu_config.keys():
			retval[j]['mtu'] =  mtu_config[j]
		if j in addr.keys():
			retval[j]['addr'] =  addr[j]
		if j in prefix.keys():
			retval[j]['prefix'] =  prefix[j]
	return retval, bridge

def get_net_config_gw(d1):
	gw_net_config={}
	static_config={}
	mtu_config={}
	retval = {}
	for i in d1['vm']['gw']['interfaces'].keys():
		if 'family' in d1['vm']['gw']['interfaces'][i].keys():
			if i.replace('em','eth') not in gw_net_config.keys():
				gw_net_config[i.replace('em','eth')]=[]
			if 'inet' in d1['vm']['gw']['interfaces'][i]['family'].keys():
				gw_net_config[i.replace('em','eth')].append(d1['vm']['gw']['interfaces'][i]['family']['inet'])
			if 'inet6' in d1['vm']['gw']['interfaces'][i]['family'].keys():
				gw_net_config[i.replace('em','eth')].append(d1['vm']['gw']['interfaces'][i]['family']['inet6'])
			if 'static' in d1['vm']['gw']['interfaces'][i]['family'].keys():
				static_config[i.replace('em','eth')]=d1['vm']['gw']['interfaces'][i]['family']['static']
		if 'mtu' in d1['vm']['gw']['interfaces'][i].keys():
			mtu_config[i.replace('em','eth')]=d1['vm']['gw']['interfaces'][i]['mtu']
	intf_list = []
	for i in d1['vm']['gw']['interfaces'].keys():
		if i != 'em0':
			j = i.replace('em','eth')
			retval[j]={
				'addresses': None,
				'static': None,
				'mtu': None
			}
	for j in retval.keys():
		if j in gw_net_config.keys():
			retval[j]['addresses']=gw_net_config[j]
		if j in static_config.keys():
			retval[j]['static'] =  static_config[j]
		if j in mtu_config.keys():
			retval[j]['mtu'] =  mtu_config[j]
	return retval


def get_subnet(ipv4):
	mask_full = (0xFF << 24 ) + (0xFF << 16) + (0xFF << 8) + 0xFF
	b1,b2,b3,b4 = ipv4.split('/')[0].split('.')
	ip_bin= (int(b1) << 24) + (int(b2) << 16) + (int(b3) << 8) + int(b4)
	mask_bin = mask_full << (32 - int(ipv4.split('/')[1]))
	subnet_bin = ip_bin & mask_bin
	subnet = bin2quad(subnet_bin)
	netmask = bin2quad(mask_bin)
	return subnet, netmask 

def bin2quad(binvalue):
	m1 = 255<<24
	m2 = 255<<16
	m3 = 255 << 8
	m4 = 255
	b1=str((binvalue & m1) >> 24)
	b2=str((binvalue & m2) >> 16)
	b3=str((binvalue & m3) >> 8)
	b4=str(binvalue & m4)
	retval = '.'.join((b1,b2,b3,b4))
	#print(retval)
	return retval

# def test(d1):
# 	print("this is a test")
# 	dhcp_config,net_config = get_dhcp_server_config(d1)
# 	print("dhcp_config")
# 	print(dhcp_config)

# def change_dhcp(d1):
# 	dhcp_config, net_config = get_dhcp_config(d1)
# 	line_to_file = ['#!/bin/bash']
# 	line_to_file += ['cat << EOF | sudo tee /etc/dhcp/dhcpd.conf']
# 	line_to_file += dhcp_config
# 	line_to_file += ['EOF']
# 	line_to_file += ['']
# 	line_to_file += ['sudo systemctl restart isc-dhcp-server']
# 	f1=param1.tmp_dir + 'change_dhcp.sh'
# 	write_to_file(f1,line_to_file)
# 	ssh=connect_to_gw(d1)
# 	sftp=ssh.open_sftp()
# 	print("uploading file to gw")
# 	sftp.put(f1,'change_dhcp.sh')
# 	print("Executing script on gw")
# 	print("chmod +x change_dhcp.sh")
# 	cmd1="chmod +x /home/ubuntu/change_dhcp.sh"
# 	s0,s1,s2=ssh.exec_command(cmd1)
# 	cmd1="bash /home/ubuntu/change_dhcp.sh"
# 	print("executing change_dhcp.sh")
# 	ssh.exec_command(cmd1)
# 	sftp.close()
# 	ssh.close()

def set_gw_v2(d1):
	# this function work with kea-dhcp4-server
	print("Creating configuration for node GW")
	set_gw_param = get_dhcp_config(d1)
	#pprint.pprint(set_gw_param['dhcp'])
	with open(d1['template']['kea_dhcp4']) as f1:
		t1=f1.read()
	kea4_script=Template(t1).render(set_gw_param['dhcp'])
	kea4=yaml.load(kea4_script,Loader=yaml.FullLoader)
	#kea4=yaml.safe_load(kea4_script)
	# with open("tmp/kea-dhcp4.yaml","w") as f1:
	# 	f1.write(kea4_script)
	# with open("tmp/kea-dhcp4.yaml") as f1:
	# 	kea4=yaml.load(f1,Loader=yaml.FullLoader)
	# vm_list = []
	# for i in set_gw_param['dhcp']['vm']:
	# 	vm = {
	# 		'hostname' : i, 
	# 		'hw-address': set_gw_param['dhcp']['vm'][i]['mac'], 
	# 		'ip-address': set_gw_param['dhcp']['vm'][i]['ip']
	# 	}
	# 	if set_gw_param['dhcp']['vm'][i]['type'] == 'junos':
	# 		vm['option-data'] = [
	# 			{ 'name': 'vendor-encapsulated-options'},
	# 			{
	# 				'data': i + '.conf',
	# 				'name': 'config-file-name',
	# 				'space': 'vendor-encapsulated-options-space'
	# 			},
	# 			{
	# 				'data': 'tftp',
	# 				'name': 'transfer-mode',
	# 				'space': 'vendor-encapsulated-options-space'
	# 			}
	# 		]
	# 	vm_list.append(vm)
	# kea4['Dhcp4']['reservations'] = vm_list
	kea4_json = json.dumps(kea4,indent=2)
	# print(kea4_json)
	file1=param1.tmp_dir + 'kea-dhcp4.conf'
	with open(file1,"w") as f1:
		f1.write(kea4_json)
	print("uploading kea-dhcp4.conf to gw")
	ssh=connect_to_gw(d1)
	sftp=ssh.open_sftp()
	ssh.exec_command("sudo rm  ~/kea-dhcp4.conf")
	sftp.put(file1,'kea-dhcp4.conf')
	sftp.close()
	with open(d1['template']['set_gw2']) as f1:
		t1=f1.read()
	set_gw_script=Template(t1).render(set_gw_param)
	file1=param1.tmp_dir + 'set_gw.sh'
	with open(file1,"w") as f1:
		f1.write(set_gw_script)
	print("uploading set_gw.sh to gw")
	ssh=connect_to_gw(d1)
	ssh.exec_command("mkdir ~/tftp")
	sftp=ssh.open_sftp()
	sftp.put(file1,'set_gw.sh')
	sftp.close()
	for i in d1['vm'].keys():
		if d1['vm'][i]['type'] in ['vjunos_switch','vjunos_router','vjunos_evolved','vjunos_evolvedBX'] and d1['vm'][i]['ztp']:
			src1 = f"{param1.tmp_dir}{i}.conf"
			dst1 = f"tftp/{i}.conf"
			sftp=ssh.open_sftp()
			print(f"uploading file {src1} to {dst1}")
			sftp.put(src1,dst1)
			sftp.close()
	print("Executing script on gw")
	cmd1="bash ~/set_gw.sh"
	stdin_, stdout_, stderr_ = ssh.exec_command(cmd1)
	stdout_.channel.recv_exit_status()
	ssh.close()

def set_gw_v1(d1):
	# this function work with isc-dhcp4-server
	print("Creating configuration for node GW")
	set_gw_param = get_dhcp_config(d1)
	#print(set_gw_param)
	#print(f"template {d1['template']['set_gw']}")
	# junos_dhcp=[]
	# for i in d1['vm'].keys():
	# 	if 'dhcp' in d1['vm'][i].keys():
	# 		junos_dhcp.append(i)

	with open(d1['template']['set_gw']) as f1:
		t1=f1.read()
	#print(f"template {t1}")
	set_gw_script=Template(t1).render(set_gw_param)
	file1=param1.tmp_dir + 'set_gw.sh'
	#file2=param1.tmp_dir + '*.conf'
	with open(file1,"w") as f1:
		f1.write(set_gw_script)
	print("uploading file to gw")
	ssh=connect_to_gw(d1)
	ssh.exec_command("mkdir ~/tftp")
	sftp=ssh.open_sftp()
	sftp.put(file1,'set_gw.sh')
	sftp.close()
	# if junos_dhcp:
	# 	for i in junos_dhcp:
	# 		file2=file2=param1.tmp_dir + f"{i}.conf"
	# 		dst2 = f"tftp/{i}.conf"
	# 		# print(f"file2 {file2}")
	# 		# print(f"dst2 {dst2}")
	# 		print(f"upload file {i}.conf")
	# 		sftp.put(file2,dst2)
	for i in d1['vm'].keys():
		if d1['vm'][i]['type'] in ['vjunos_switch','vjunos_router','vjunos_evolved','vjunos_evolvedBX'] and d1['vm'][i]['ztp']:
			src1 = f"{param1.tmp_dir}{i}.conf"
			dst1 = f"tftp/{i}.conf"
			sftp=ssh.open_sftp()
			print(f"uploading file {src1} to {dst1}")
			sftp.put(src1,dst1)
			sftp.close()
	print("Executing script on gw")
	#print("chmod +x set_gw.sh")
	# cmd1="chmod +x /home/ubuntu/set_gw.sh"
	#cmd1='ls -la'
	#s0,s1,s2=ssh.exec_command(cmd1)
	cmd1="bash ~/set_gw.sh"
	# print("executing set_gw.sh")
	stdin_, stdout_, stderr_ = ssh.exec_command(cmd1)
	stdout_.channel.recv_exit_status()
	ssh.close()
	#print(set_gw_script)


# def get_ztp_config(d1):
# 	if 'ztp' in d1.keys():
# 		print("Creating ZTP config for apstra")
# 		filename1 = param1.tmp_dir + "ztp_config.txt"
# 		if not os.path.exists(param1.tmp_dir):
# 			os.mkdir(param1.tmp_dir)
# 		with open(d1['template']['ztp_dhcp']) as f1:
# 			jt=f1.read()
# 		ztp_data = create_ztp_config(d1)
# 		#print(ztp_data)
# 		ztp_config = Template(jt).render(ztp_data)
# 		print(f"write ztp configuration to {filename1}")
# 		with open(filename1,"w") as f1:
# 			f1.write(ztp_config)
# 		print(f"Don't forget to upload file {filename1} to ztp server")
# 		#write_to_file(f1,ztp_config)
# 	else:
# 		print("ZTP is not enabled")

# def get_vjunos_config(d1):
# 	print("creating configuration for vjunos")
# 	gw_bridge=[]
# 	dhcp_subnet=[]
# 	vm=[]
# 	for i in d1['vm'].keys():
# 		if d1['vm'][i]['type'] in ["vjunos_switch","vjunos_evolved"]:
# 			dt1={}
# 			dt1[i]=[d1['vm'][i]['interfaces']['mgmt']['family']['inet'].split('/')[0]]
# 			if d1['vm'][i]['interfaces']['mgmt']['bridge'] not in gw_bridge:
# 				gw_bridge.append(d1['vm'][i]['interfaces']['mgmt']['bridge'])
# 	for i in d1['gw']['interfaces'].keys():
# 		dt1={}
# 		if d1['gw']['interfaces'][i]['bridge'] in gw_bridge:
# 			dt1['gw']= d1['gw']['interfaces'][i]['family']['inet'].split('/')[0]
# 			dt1['subnet']= to_subnet(d1['gw']['interfaces'][i]['family']['inet'])
# 			dhcp_subnet.append(dt1)
# 	with open(d1['template']['dhcp']) as f1:
# 		jt=f1.read()

# 	if 'ztp' in d1.keys():
# 		print("Creating ZTP config for apstra")
# 		filename1 = param1.tmp_dir + "ztp_config.txt"
# 		if not os.path.exists(param1.tmp_dir):
# 			os.mkdir(param1.tmp_dir)
# 		with open(d1['template']['ztp_dhcp']) as f1:
# 			jt=f1.read()
# 		ztp_data = create_ztp_config(d1)
# 		#print(ztp_data)
# 		ztp_config = Template(jt).render(ztp_data)
# 		print(f"write ztp configuration to {filename1}")
# 		with open(filename1,"w") as f1:
# 			f1.write(ztp_config)
# 		print(f"Don't forget to upload file {filename1} to ztp server")
# 		#write_to_file(f1,ztp_config)
# 	else:
# 		print("ZTP is not enabled")

def to_subnet(s1):
	ip1=s1.split('/')[0].split('.')
	nm0=prefix2netmask(s1.split('/')[1])
	nm1=nm0.split('.')
	b=[]
	for i in list(range(4)):
		t1 = int(ip1[i]) & int(nm1[i])
		b.append(str(t1))
	r1 = '.'.join(b)
	retval = f"{r1}/{nm0}"
	return retval


def create_novnc(d1):
	print("Creating novnc")
	novnc_port = 6081
	retval={}
	vnc_list = []
	cmd1=""
	for i in d1['vm'].keys():
		if 'vnc' in d1['vm'][i].keys():
			if d1['vm'][i]['vnc'] != "no":
				vnc_list.append(i)
				retval[i]={
					'port' : novnc_port,
					'vnc_server': ''
				}
				novnc_port +=1
	print(f"vnc_list {vnc_list}")
	for i in vnc_list:
		cmd1 += f"vmm args {i} | grep \"vnc\"\n"
	#print("command")
	#print(cmd1)
	ssh=sshconnect(d1)
	# cmd1=f"vmm args {vm} | grep \"vnc\""
	_,s2,_=ssh.exec_command(cmd1)
	
	i = 0
	for j in s2.readlines():
		k = vnc_list[i]
		#print(f"vm {k}")
		vnc_server = j.strip().split()[1]
		retval[k]['vnc_server']=vnc_server
		#print(vnc_server)
		i +=1
	#print(retval)
	ssh.close()
	return retval


# def get_dns(d1):
# 	# cmd1="sudo systemd-resolve --status | grep -A1 \"DNS Servers\" | sed -e 's/DNS Servers://' | sed -e 's/ *//'"
# 	cmd1="resolvectl status | grep DNS| grep 'DNS Servers:' | cut -f 2 -d ':'"
# 	ssh=connect_to_gw(d1)
# 	print(f"executing command {cmd1}")
# 	print("Getting ip addresses of DNS server")
# 	stdin, stdout, stderr = ssh.exec_command(cmd1)
# 	output=stdout.read()
# 	#print(f"output {output}")
# 	a=output.strip().decode("utf-8").replace(" ",":").split(":")
# 	# dns=[]
# 	# for i in a:
# 	# 	if i:
# 	# 		dns.append(i)
# 	# #dns=['8.8.8.8','8.8.4.4']
# 	# if len(a)>2:
# 	# 	dns = dns[0:2]
# 	# print(f"dns {dns}")

# 	d1['pod']['dns']=param1.jnpr_dns
# 	# print(f"DNS1 {d1['pod']['dns'][0]}")
# 	# print(f"DNS2 {d1['pod']['dns'][1]}")
# 	ssh.close()

# def iscsi_initiator():
# 	# file /etc/iscsi/initiatorname.iscsi
# 	# tmp1="InitiatorName=iqn.1993-08.org.debian:01:895b5c8"
# 	_,a=str(hex(random.randint(0x1000,0xffff))).split('x')
# 	tmp1="iqn.2004-10.com.ubuntu:01:60f35178" + a
# 	return tmp1


def set_host(d1,vm=""):
	host_yes=['centos','rhel','ubuntu','ubuntu2','debian','bridge','desktop']
	list_hosts=[]
	#get_dns(d1)
	filename1=param1.tmp_dir + 'set_host.sh'
	if vm:
		if vm not in d1['vm'].keys():
			print(f"host {vm} is not on the topology")
		else:
			if d1['vm'][vm]['os'] not in host_yes:
				print(f"host {vm} OS is not supported yet")
			else:
				list_hosts.append(vm)		
	else:
		for i in d1['vm'].keys():
			if d1['vm'][i]['os'] in host_yes:
				if  'family' in d1['vm'][i]['interfaces']['em0'].keys():
					if  'inet' in d1['vm'][i]['interfaces']['em0']['family'].keys():
						list_hosts.append(i)
	print(f"setting VM {list_hosts}")
	for i in list_hosts:
		#print(f"host {i}")
		vm_data={}
		vm_data['net'],vm_data['bridge'] = get_net_config(d1,i)
		vm_data['dns_ip']=get_dns_ip(d1,i)
		# vm_data['ip_gw'] = d1['vm']['gw']['interfaces']['em1']['family']['inet'].split('/')[0]
		vm_data['ssh_key_pub'] = d1['pod']['ssh_key_host']
		vm_data['ssh_key_priv'] = d1['pod']['ssh_key_host_priv']
		vm_data['hostname'] = i
		# print(f"host {i} {vm_data}")
		#if d['vm'][i]['os'] == 'ubuntu':
		if d1['vm'][i]['os'] in ["ubuntu","ubuntu2","desktop"]:
			tfile = "ubuntu"
		elif d1['vm'][i]['os'] == 'debian':
			tfile = "debian"
		elif d1['vm'][i]['os'] in  ['centos','rhel']:
			tfile = "centos"
		elif d1['vm'][i]['os'] == 'bridge':
			tfile = "bridge"
		else:
			tfile = False
		#print(f"tfile {tfile}")
		if tfile:
			with open(d1['template'][tfile]) as f1:
				t1 = f1.read()
			#print(t1)
			c1 = Template(t1).render(vm_data)
			# print(vm_data)
			#print(c1)
			with open(filename1,"w") as f1:
				f1.write(c1)
			ssh2host=connect_to_vm(d1,i)
			sftp=ssh2host.open_sftp()
			print(f"uploading file to {i}" )
			sftp.put(filename1,'set_host.sh')
			print(f"Executing script on {i}")
			#cmd1="chmod +x /home/ubuntu/set_host.sh"
			#cmd1="chmod +x ~/set_host.sh"
			#ssh2host.exec_command(cmd1)
			#cmd1="bash /home/ubuntu/set_host.sh"
			#cmd1="nohup sh ~/set_host.sh &"
			cmd1="sh ~/set_host.sh"
			stdin_, stdout_, stderr_ = ssh2host.exec_command(cmd1)
			# stdout_.channel.recv_exit_status()
			# sftp.close()
			# ssh2host.close()
	
def get_dns_ip(d1,i):
	retval='127.0.1.1'
	if 'family' in d1['vm'][i]['interfaces']['em0'].keys():
		if 'inet' in d1['vm'][i]['interfaces']['em0']['family'].keys():
			retval = d1['vm'][i]['interfaces']['em0']['family']['inet'].split('/')[0]
	return retval

def get_gateway(d1,i):
	retval=''
	bridge1 = d1['vm'][i]['interfaces']['em0']['bridge']
	for j in d1['vm']['gw']['interfaces'].keys():
		if bridge1 == d1['vm']['gw']['interfaces'][j]['bridge']:
			retval=d1['vm']['gw']['interfaces'][j]['family']['inet'].split('/')[0]
	return retval
	
def get_vjunos_mac(d1):
	#print("inside get_vjunos_mac")
	mac_vjunos = get_mac_vjunos(d1)
	pprint.pprint(mac_vjunos)

def get_mac_vjunos(d1):
	mac_vjunos={}
	#print("inside one")
	#print(d1['vm'].keys())
	for i in d1['vm'].keys():
		# if d1['vm'][i]['os'] == 'vjunos_switch':
		if d1['vm'][i]['os'] == 'vjunos_router' or d1['vm'][i]['os'] == 'vjunos_switch' or d1['vm'][i]['os'] == 'evo' or d1['vm'][i]['os'] == 'vjunos_evolved' or d1['vm'][i]['os'] == 'vjunos_evolvedBX':
			print(f"Getting mac of {i}")
			mac_vjunos[i]={}
			mac_vjunos[i]['mac']=get_mac_vm(d1,i)
			mac_vjunos[i]['ip']=d1['vm'][i]['interfaces']['mgmt']['family']['inet'].split('/')[0]
	return mac_vjunos

def create_ztp_config(d1):
	print("Getting vjunos mac address")
	mac_vjunos = get_mac_vjunos(d1)
	retval={}
	if mac_vjunos and 'ztp' in d1.keys():
		retval['ztp_server'] = d1['ztp']['server']
		retval['subnet']=[]
		retval['host']=[]
		for i in d1['ztp']['subnet']:
			retval['subnet'].append({
				'subnet' : i['subnet'].split('/')[0],
				'netmask':  prefix2netmask(i['subnet'].split('/')[1]),
				'routers': i['gateway'],
				'low_ip': i['range'][0],
				'high_ip' : i['range'][1]
			})
		for i in mac_vjunos.keys():
			retval['host'].append(
				{
					'host' : i,
					'mac' : mac_vjunos[i]['mac'],
					'ip': mac_vjunos[i]['ip']
				}
			)
	return retval

def get_mac_vm(d1,i):
	if d1['pod']['type'] == 'vmm':
		if d1['vm'][i]['os'] == 'evo':
			vm = f"{i}_RE0"
		else: 
			vm = i
		ssh=sshconnect(d1)
		cmd1="vmm args " + vm + " | grep \" mac \""
		stdin,stdout,sstderr=ssh.exec_command(cmd1)
		j = stdout.readlines()
		ssh.close()
		_,retval= j[0].rstrip().split()
		return retval

	elif d1['pod']['type'] == 'kvm':
		print("not implemented for this type")
		return ""
	
def get_vjunos_sernum(d1,i):
	cmd1=f"cli -c \"show chassis hardware | match Chassis\" | tr -s \" \" | cut -d \" \" -f 2"

def get_serial(d1,vm=""):
	if d1['pod']['type'] == 'vmm':
		ssh=sshconnect(d1)
		print('-----')
		print("serial port of VM")
		cmd1="vmm list"
		s1,s2,s3=ssh.exec_command(cmd1)
		vm_list=[]
		for i in s2.readlines():
			vm_list.append(i.rstrip().split()[0])	
		if vm=="":
			print("vm list", vm_list)
			for i in vm_list:
				print("serial of " + i + " : " + get_serial_vm(d1,i).replace(":"," "))
		elif vm not in vm_list:
			print("VM %s does not exist " %(vm))
		else:
			print("serial of " + vm + " : " + get_serial_vm(d1,vm).replace(":"," "))
		ssh.close()
	elif d1['pod']['type'] == 'kvm':
		print("not yet implemented")


def get_serial_vm(d1,i):
	ssh=sshconnect(d1)
	cmd1="vmm args " + i + " | grep \"serial \""
	s1,s2,s3=ssh.exec_command(cmd1)
	j=s2.readlines()[0]
	return j.rstrip().split()[1]

def list_vm(d1):
	if d1['pod']['type'] == 'vmm':
		print('list of running VM')
		ssh=sshconnect(d1)
		print('-----')
		cmd1="vmm list"
		s1,s2,s3=ssh.exec_command(cmd1)
		for i in s2.readlines():
			print(i.rstrip())
		ssh.close()
	elif d1['pod']['type'] == 'kvm':
		print("not yet implemented")

def stop(d1):
	if d1['pod']['type'] == 'vmm':
		ssh=sshconnect(d1)
		print('-----')
		print("stop the existing topology")
		cmd1="vmm stop && vmm unbind"
		s1,s2,s3=ssh.exec_command(cmd1)
		for i in s2.readlines():
			print(i.rstrip())
		ssh.close()
	elif d1['pod']['type'] == 'kvm':
		print("not yet implemented")

# def check_vsan_status(d1):
# 	retval = False
# 	for i in d1['vm'].keys():
# 		if d1['vm'][i]['type'] == 'vcsa':
# 			if 'vsan' in d1['vm'][i].keys():
# 				if d1['vm'][i]['vsan'] == 'yes' or d1['vm'][i]['vsan']:
# 					retval = True
# 			break
# 	return retval

# def create_esxi_disk(d1,ssh):
# 	# print("create esxi disk")
# 	# vsan_disk = check_vsan_status(d1)
# 	if check_vsan_status(d1):
# 		for i in d1['vm'].keys():
# 			if d1['vm'][i]['os'] == 'esxi':
# 				disk_name = 'esxi' + str(d1['vm'][i]['disk']) + ".vmdk"
# 				# str1= d1['pod']['home_dir'] + "/" + d1['images'][disk_name]
# 				str1 = d1['pod']['home_dir'] +'/vm/' + d1['name'] + "/" + disk_name
# 				# str1= d1['pod']['home_dir'] +'/vm/' + d1['name'] + "/" + d1['images'][disk_name]
# 				cmd2 = "qemu-img create -f vmdk " + str1.replace(".vmdk","disk2.vmdk") + " " + str(param1.esxi_ds_size) + "G"
# 				cmd3 = "qemu-img create -f vmdk " + str1.replace(".vmdk","disk3.vmdk") + " " + str(param1.esxi_ds_size) + "G"
# 				s1,s2,s3=ssh.exec_command(cmd2)
# 				for i in s2.readlines():
# 					print(i.rstrip())
# 				s1,s2,s3=ssh.exec_command(cmd3)
# 				for i in s2.readlines():
# 					print(i.rstrip())

def create_hd2(d1):
	#os_type=['ubuntu','ubuntu2','centos','debian','pa2']
	dest_dir=d1['pod']['home_dir'] +'/vm/' + d1['name'] + "/"
	vm_with_hd2 = {}
	vm_with_hd3 = {}
	for i in d1['vm'].keys():
		# if d1['vm'][i]['os'] in os_type:
		# 	if 'hd2' in d1['vm'][i].keys():
		# 		vm_with_hd2[i]=d1['vm'][i]['hd2']
		# 	if 'hd3' in d1['vm'][i].keys():
		# 		vm_with_hd3[i]=d1['vm'][i]['hd3']
		if 'hd2' in d1['vm'][i].keys():
			vm_with_hd2[i]=d1['vm'][i]['hd2']
		if 'hd3' in d1['vm'][i].keys():
			vm_with_hd3[i]=d1['vm'][i]['hd3']
	cmd_list=""
	if vm_with_hd2:
		for i in vm_with_hd2.keys():
			ds=vm_with_hd2[i]
			# str_tmp1 = f"qemu-img create -f vmdk {dest_dir}{i}_disk2.img {ds}"
			str_tmp1 = f"qemu-img create -f qcow2 {dest_dir}{i}_disk2.img {ds}"
			cmd_list += f"{str_tmp1};"
	if vm_with_hd3:
		for i in vm_with_hd3.keys():
			ds=vm_with_hd3[i]
			# str_tmp1 = f"qemu-img create -f vmdk {dest_dir}{i}_disk3.img {ds}"
			str_tmp1 = f"qemu-img create -f qcow2 {dest_dir}{i}_disk3.img {ds}"
			cmd_list += f"{str_tmp1};"
	#print("create disk2 and disk3")
	#print(cmd_list)
	return cmd_list
		
def start(d1):
	if d1['pod']['type'] == 'vmm':
		print('starting topology on vmm')
		lab_conf=d1['pod']['home_dir'] +'/vm/' + d1['name'] + "/lab.conf"
		ssh=sshconnect(d1)
		print('-----')
		print("stop and unbind the existing topology")
		
		#print(cmd1)
		# if cmd1:
		# 	s1,s2,s3=ssh.exec_command(cmd1)
		# 	for i in s2.readlines():
		# 		print(i.rstrip())
		cmd1="vmm stop"
		s1,s2,s3=ssh.exec_command(cmd1)
		for i in s2.readlines():
			print(i.rstrip())
		cmd1="vmm unbind"
		s1,s2,s3=ssh.exec_command(cmd1)
		for i in s2.readlines():
			print(i.rstrip())
		# cmd1 = check_disk2(d1)
		# print("create hd2/hd3 ")
		cmd1=create_hd2(d1)
		if cmd1:
			print("creating secondary disk")
			# time.sleep(3)
			s1,s2,s3=ssh.exec_command(cmd1)
			for i in s2.readlines():
				print(i.rstrip())
			time.sleep(3)
		print("start configuration ")
		#create_esxi_disk(d1,ssh)
		cmd1=f"vmm config {lab_conf} -g {param1.vmm_group}"
		s1,s2,s3=ssh.exec_command(cmd1)
		for i in s2.readlines():
			print(i.rstrip())
		print("start topology ")
		cmd1="vmm start"
		s1,s2,s3=ssh.exec_command(cmd1)
		for i in s2.readlines():
			print(i.rstrip())
		write_ssh_config(d1)
		ssh.close()
		
	elif d1['pod']['type'] == 'kvm':
		print("not yet implemented")

# def check_disk2(d1):
# 	d2 =[]
# 	for i in d1['vm'].keys():
# 		if d1['vm'][i]['os'] == 'pa2':
# 			d2.append(f"qemu-img create -f qcow2 {i}_disk2.img 50G")
# 	return d2
def check_disk2(d1):
	d2 =""
	for i in d1['vm'].keys():
		if d1['vm'][i]['os'] == 'pa2':
			dsk2 = f"{d1['pod']['home_dir']}/vm/{d1['name']}/{i}_disk2.img"
			d2 += f"qemu-img create -f vmdk {dsk2} 50G;"
	return d2

def upload(d1,upload_status=1):
	if d1['pod']['type'] == 'vmm':
		if upload_status:
			print('starting topology on vmm')
		else:
			print('creating topology for  vmm')
		if not checking_config_syntax(d1):
			return
		with open(d1['template']['vmmtopo']) as f1:
			t1=f1.read()
		datatopo=create_lab_config(d1)
		#print(f"datatopo {datatopo}")
		c1 = Template(t1).render(datatopo)
		#print(datatopo)
		#print(c1)
		if os.path.exists(param1.tmp_dir):
			print("directory exist ")
			shutil.rmtree(param1.tmp_dir)
		os.mkdir(param1.tmp_dir)
		f1=param1.tmp_dir + "lab.conf"
		with open(f1,"w") as wr1:
			wr1.write(c1)
		write_junos_config(d1)
		write_pc_dummy_config(d1)
		# write_inventory(d1)
		# if 'ztp' in d1.keys():
		# 	f1 = param1.tmp_dir + "ztp_config.txt"
		# 	ztp_config = create_ztp_config(d1)
		# 	write_to_file(f1,ztp_config)

		# cmd1=create_hd2(d1)
		# if cmd1:
		# 	ssh=sshconnect(d1)
		# 	print("creating secondary disk")
		# 	s1,s2,s3=ssh.exec_command(cmd1)
		# 	for i in s2.readlines():
		# 		print(i.rstrip())
		
		if upload_status:
			upload_file_to_server(d1)
	elif d1['pod']['type'] == 'kvm':
		print("not yet implemented")

def write_pc_dummy_config(d1):
	for i in d1['vm'].keys():
		if d1['vm'][i]['type'] in param1.pc_type:
			f1=param1.tmp_dir + i + ".conf"
			with open(f1,"w") as wr1:
				wr1.write(" ")

def create_lab_config(d1):
	os_list=[]
	#retval = False
	for i in d1['vm'].keys():
		if d1['vm'][i]['os'] not in os_list:
			os_list.append(d1['vm'][i]['os'])
	#print(d1['images'].keys())
	image_list=d1['images'].keys()
	disk={}
	for i in os_list:
		if i in ['vmx','mx240','mx480','mx960']:
			if 'vmx' in image_list:
				disk['vmx']=f"{d1['pod']['home_dir']}/{d1['images']['vmx']}"
		else:
			if i in image_list:
				disk[i] = f"{d1['pod']['home_dir']}/{d1['images'][i]}"
	#print(disk,disk['gw'])
	d2={}
	d2['disk']=disk
	d2['name']=d1['name']
	d2['bridge']=list_of_bridge(d1)
	d2['vm']={}
	for i in d1['vm'].keys():
		type = d1['vm'][i]['type']
		dsk = d1['vm'][i]['os']
		#print(f"type {type}, disk {disk[dsk]}")
		#print(param1.vm_type)
		path1 = f"{d1['pod']['home_dir']}/vm/{d1['name']}/{i}.conf"
		#print(f"path1 ")
		dsk2 = f"{d1['pod']['home_dir']}/vm/{d1['name']}/{i}_disk2.img"
		dsk3 = f"{d1['pod']['home_dir']}/vm/{d1['name']}/{i}_disk3.img"
		if not d2['vm']:
			# if d1['vm'][i]['os'] == 'pa2':
			# 	d2['vm']={i : { 'type': param1.vm_type[type], 'disk': dsk,'disk2': dsk2,  'install':path1, 'intf':{}}}
			# else:
			# 	if 'hd2' in d1['vm'][i].keys():
			# 		if 'hd3' in d1['vm'][i].keys():
			# 			print(f"vm ${i} has hd3")
			# 			d2['vm']={i : { 'type': param1.vm_type[type], 'disk': dsk,'disk2': dsk2,'disk3':dsk3,'install':path1, 'intf':{}}}
			# 		else:
			# 			d2['vm']={i : { 'type': param1.vm_type[type], 'disk': dsk,'disk2': dsk2,'install':path1, 'intf':{}}}
			# 	else:
			# 		d2['vm']={i : { 'type': param1.vm_type[type], 'disk': dsk, 'install':path1, 'intf':{}}}
			if 'hd2' in d1['vm'][i].keys():
				if 'hd3' in d1['vm'][i].keys():
					print(f"vm ${i} has hd3")
					d2['vm']={i : { 'type': param1.vm_type[type], 'disk': dsk,'disk2': dsk2,'disk3':dsk3,'install':path1, 'intf':{}}}
				else:
					d2['vm']={i : { 'type': param1.vm_type[type], 'disk': dsk,'disk2': dsk2,'install':path1, 'intf':{}}}
			else:
				d2['vm']={i : { 'type': param1.vm_type[type], 'disk': dsk, 'install':path1, 'intf':{}}}
		else:
			# if d1['vm'][i]['os'] == 'pa2':
			# 	d2['vm'][i]={ 'type': param1.vm_type[type], 'disk': dsk, 'disk2': dsk2,'install':path1,'intf':{}}
			# else:
			# 	if 'hd2' in d1['vm'][i].keys():
			# 		if 'hd3' in d1['vm'][i].keys():
			# 			d2['vm'][i]={ 'type': param1.vm_type[type], 'disk': dsk,'disk2': dsk2,'disk3':dsk3,'install':path1, 'intf':{}}
			# 		else:
			# 			d2['vm'][i]={ 'type': param1.vm_type[type], 'disk': dsk,'disk2': dsk2,'install':path1, 'intf':{}}
			# 	else:
			# 		d2['vm'][i]={ 'type': param1.vm_type[type], 'disk': dsk, 'install':path1,'intf':{}}
			if 'hd2' in d1['vm'][i].keys():
				if 'hd3' in d1['vm'][i].keys():
					d2['vm'][i]={ 'type': param1.vm_type[type], 'disk': dsk,'disk2': dsk2,'disk3':dsk3,'install':path1, 'intf':{}}
				else:
					d2['vm'][i]={ 'type': param1.vm_type[type], 'disk': dsk,'disk2': dsk2,'install':path1, 'intf':{}}
			else:
				d2['vm'][i]={ 'type': param1.vm_type[type], 'disk': dsk, 'install':path1,'intf':{}}
		intf_list={}
		if 'efi' in d1['vm'][i].keys():
			if d1['vm'][i]['efi'] == 'yes' or d1['vm'][i]['efi']:
				d2['vm'][i]['efi'] = 1
				#print(f"host {i}  has efi, value of efi {d2['vm'][i]['efi']}")
		#if d1['vm'][i]['type'] in param1.pc_type:
		k = 0
		#print(f"vm {i}")

		if 'vnc' in d1['vm'][i].keys():
			if d1['vm'][i]['vnc']:
				d2['vm'][i].update({'vnc':True})
		for j in  d1['vm'][i]['interfaces'].keys():
			#print(f"interface {j}")
			# if d1['vm'][i]['type'] in param1.pc_type:
			# 	intf_t1 = f"em{k}"
			# 	k+=1
			# else:
			# 	intf_t1 = f"vio{k}"
			# 	k+=1
			# if not intf_list:
			# 	intf_list={intf_t1 : d1['vm'][i]['interfaces'][j]['bridge'] }
			# else:
			# 	intf_list[intf_t1]= d1['vm'][i]['interfaces'][j]['bridge']
			if j not in ["lo","lo0"]:
				if d1['vm'][i]['type'] in param1.pc_type:
					intf1 = j
				elif d1['vm'][i]['type'] in param1.junos_type:
					if d1['vm'][i]['type'] in ['vmx','mx240','mx480','mx960']:
						if j == 'mgmt':
							intf1 = 'em0'
						else:
							idx = j.split('/')[2]
							intf1 = f"GE(0,0,{idx})"
					else:
						if j == 'mgmt':
							intf1 = 'vio0'
						elif j.split('-')[0] in ['ge','et','xe']:
							# if d1['vm'][i]['type'] == 'vjunos_evolved' or d1['vm'][i]['type'] == 'vjunos_evolvedBX':
							# 	if 'vm_type' in d1['vm'][i].keys():
							# 		if d1['vm'][i]['vm_type'] == 0:
							# 			idx = int(j.split('/')[2]) + 5
							# 		else:
							# 			idx = int(j.split('/')[2]) + 1
							# 	else:
							# 		idx = int(j.split('/')[2]) + 1
							# else:
							# 	idx = int(j.split('/')[2]) + 1
							idx = int(j.split('/')[2]) + 1
							intf1 = f"vio{idx}"
						else:
							intf1=j
				if not intf_list:
					intf_list={intf1 : d1['vm'][i]['interfaces'][j]['bridge'] }
				else:
					intf_list[intf1]= d1['vm'][i]['interfaces'][j]['bridge']
		d2['vm'][i]['intf']=dict(sorted(intf_list.items()))
		#print(d2['vm'][i]['intf'])
	return d2

# def add_evo1(d1):
# 	retval=[]
# 	retval.append('#undef EVOvArdbegRE')
# 	retval.append('#define EVOvArdbegRE(CHAS_NAME,BOOT_DISK) \\')
# 	retval.append('    bridge XCAT(CHAS_NAME, _FPC0_RPIO_BRG) {};\\')
# 	retval.append('    bridge XCAT(CHAS_NAME, _FPC0_PFE_BRG) {};\\')
# 	retval.append('    vm STRINGIZE (CATENATE3 (CHAS_NAME, _RE, EVOVPTX_RE0)) {\\')
# 	retval.append('    hostname XCAT(CHAS_NAME, _node0);\\')
# 	retval.append('    cdrom_boot BOOT_DISK;\\')
# 	retval.append('    memory EVOvArdbeg_RE_MEMORY;\\')
# 	retval.append('    ncpus EVOvArdbeg_RE_NCPU;\\')
# 	retval.append('    REsetvar(CHAS_NAME)\\')
# 	retval.append('    REinstall\\')
# 	retval.append('    interface "em0" {\\')
# 	retval.append('        bridge "{}";\\'.format(d1['pod']['evo']))
# 	retval.append('        ext_vlanid 0;\\')
# 	retval.append('    };\\')
# 	retval.append('    interface "em1" {\\')
# 	retval.append('        bridge XCAT(CHAS_NAME, _FPC0_PFE_BRG);\\')
# 	retval.append('        ext_vlanid 0;\\')
# 	retval.append('    };\\')
# 	retval.append('    interface "em2" {\\')
# 	retval.append('        bridge XCAT(CHAS_NAME, _FPC0_RPIO_BRG);\\')
# 	retval.append('            ext_vlanid 0;\\')
# 	retval.append('    };\\')
# 	retval.append('    interface "em3" {\\')
# 	retval.append('        bridge XCAT(CHAS_NAME, _FPC0_RPIO_BRG);\\')
# 	retval.append('            ext_vlanid 0;\\')
# 	retval.append('    };\\')
# 	retval.append('    interface "em4" {\\')
# 	retval.append('        bridge "{}";\\'.format(d1['pod']['evo']))
# 	retval.append('            ext_vlanid 0;\\')
# 	retval.append('    };\\')
# 	retval.append('}; ')
# 	return retval 

def write_inventory(d1):
	print("writing inventory for ansible")
	f1=param1.tmp_dir + "inventory"
	line1=["[all]"]
	for i in d1['vm'].keys():
		if d1['vm'][i]['type'] == 'junos':
			line1.append(i)
	# line1.append("[all:vars]")
	# line1.append("ansible_python_interpreter=/usr/bin/python3")
	write_to_file(f1,line1)

def write_ssh_config(d1):
	data1={}
	# jumphost_stat = False
	print("writing file ssh_config")
	for i in d1['vm'].keys():
		if d1['vm'][i]['type']=='gw':
			gw_name = i
			break
	# if 'ssh_key_name' in d1['pod'].keys():
	# 	ssh_key = d1['pod']['ssh_key_name']
	# else:
	# 	ssh_key = "id_rsa"
	# if 'ssh_key_host_name' in d1['pod'].keys():
	# 	ssh_key_host = d1['pod']['ssh_key_host_name']
	# else:
	# 	ssh_key_host = ssh_key
	# if 'jumpserver' in d1['pod'].keys():
	# 	jumphost_stat = True
	print("getting gw ip address")
	gw_ip = get_ip_vm(d1,'gw')
	print(f"ip address gw {gw_ip}")
	# if 'proxy' in d1.keys():
	# 	if 'DynForward' in d1['proxy'].keys():
	# 		dyn_port = d1['proxy']['DynForward']
	# 	else:
	# 		dyn_port = 1080
	# 	list1=[]
	# 	if 'forward' in d1['proxy'].keys():
	# 		for j in d1['proxy']['forward']:
	# 			list1.append(f"{j['localPort']} {j['destIP']}:{j['destPort']}")
	# 	forward_port = list1
	# else:
	# 	dyn_port = 1080
	# 	forward_port=[]
	node = {}
	for i in d1['vm'].keys():
		if i != 'gw':
			if 'mgmt' in d1['vm'][i]['interfaces'].keys():
				intf = 'mgmt'
			elif 'em0' in d1['vm'][i]['interfaces'].keys():
				intf = 'em0'
			else:
				intf =""
			if intf:
				user=get_ssh_user(d1,i)
				if 'family' in d1['vm'][i]['interfaces'][intf].keys():
					if not node:
						node={ i : {
	    					'ip': d1['vm'][i]['interfaces'][intf]['family']['inet'].split('/')[0],
						    'user': user }
						}
					else:
						node[i]={
							'ip': d1['vm'][i]['interfaces'][intf]['family']['inet'].split('/')[0],
							'user': user
						}
	user = get_ssh_user(d1,'gw')
	if 'jumpserver' in d1['pod'].keys():
		#js_temp = d1['pod']['jumpserver']
		js_temp = d1['pod']['vmmserver']
	else:
		js_temp = None
	# data1={
	# 	'jumphost' : js_temp,
	# 	'user' : d1['pod']['user'],
	# 	'ssh_key': ssh_key,
	# 	'ssh_key_host': ssh_key_host,
	# 	'vmm': d1['pod']['vmmserver'],
	# 	'gw': {'ip': gw_ip, 'user':user },
	# 	'node': node
	# 	}
	data1={
		'jumphost' : js_temp,
		'user' : d1['pod']['user'],
		'ssh_key_host': d1['name'],
		'vmm': d1['pod']['vmmserver'],
		'gw': {'ip': gw_ip, 'user':user },
		'node': node
		}
	#print(data1)
	with open(d1['template']['ssh_config']) as f1:
		t1 = f1.read()
	c1 = Template(t1).render(data1)
	#print(c1)
	print("write ssh_config")
	f1=param1.tmp_dir + "ssh_config"
	if not os.path.exists(param1.tmp_dir):
		os.mkdir(param1.tmp_dir)
	with open(f1,"w") as wr1:
		wr1.write(c1)
	#write_to_file(f1,c1)
	add_to_ssh_config(c1)
	#return c1

def add_to_ssh_config(file1):
	ssh_config = os.path.expanduser('~') + "/.ssh/config"
	orig1 = []
	if os.path.exists(ssh_config):
		with open(ssh_config) as f_config:
			for line in f_config:
				if '### by vmm-v3-script ###' in line:
				#if '### the last line' in line:
					print("found entry with ### by vmm-v3-script ###")
					#print("the last line")
					#orig1.append(line.rstrip())
					break
				else:
					orig1.append(line.rstrip())
		#orig1.append("\n")
		last_line = orig1[-1].replace(' ','')
		if last_line:
			orig1.append("\n")
		orig2 = "\n".join(orig1)
		with open(ssh_config,"w") as wr1:
			wr1.write(orig2)
		with open(ssh_config,"a") as wr1:
			wr1.write(file1)
	else:
		with open(ssh_config,"w") as wr1:
			wr1.write(file1)

				
def get_ip_mgmt(d1,i):
	retval=""	
	if d1['vm'][i]['type'] not in ['gw','vspirent']:
		for j in d1['vm'][i]['interfaces'].keys():
			if j == 'em0' or j=='fxp0' or j=='mgmt':
			# if d1['vm'][i]['interfaces'][j]['bridge']=='mgmt':
				if 'family' in d1['vm'][i]['interfaces'][j].keys():
					if 'inet' in d1['vm'][i]['interfaces'][j]['family'].keys():
						retval = d1['vm'][i]['interfaces'][j]['family']['inet'].split("/")[0]
	return retval

def get_ssh_user(d1,i):
	retval="" 
	if d1['vm'][i]['type'] in param1.junos_type:
		retval=d1['junos_login']['login']
	else:
		# if d1['vm'][i]['os'] == 'centos' or d1['vm'][i]['os'] == 'centosx':
		if 'centos' in d1['vm'][i]['os']:
			retval="centos"
		# elif d1['vm'][i]['os'] == 'ubuntu' or d1['vm'][i]['os'] == 'ubuntu1804':
		elif d1['vm'][i]['os'] in ['ubuntu','ubuntu2','desktop','gw']:
			retval="ubuntu"
		elif 'debian' in d1['vm'][i]['os']:
			retval="debian"
		elif 'jspace' in d1['vm'][i]['os']:
			retval="admin"
		elif d1['vm'][i]['os'] in ['aos','aos_ztp']:
			retval="admin"
		elif d1['vm'][i]['os'] in ['bridge','alpine']:
			retval="alpine"
		elif d1['vm'][i]['os'] =='rhel':
			retval="rhel"
		elif d1['vm'][i]['os'] =='pa2':
			retval="root"
		else:
			retval = 'admin'
	return retval


def upload_file_to_server(d1):
	vm_dir=d1['pod']['home_dir'] + '/vm/'
	config_dir=d1['pod']['home_dir'] + '/vm/' + d1['name'] + "/"
	#check_dir="if [ ! -d " + vm_dir + " ]; then mkdir " + vm_dir +"; fi"
	check_dir="mkdir " + vm_dir
	#ssh=paramiko.SSHClient()
	#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# ssh.connect(hostname=d1['pod']['server'],username=d1['pod']['user'])
	#ssh.connect(hostname=d1['pod']['server'],username=d1['pod']['user'],password=d1['pod']['password'])
	ssh=sshconnect(d1)
	sftp=ssh.open_sftp()
	cmd1="rm -rf " + config_dir
	#print("check directory ",vm_dir)
	#print("command ",check_dir)
	#ssh.exec_command(check_dir)
	print("deleting config_dir " , config_dir)
	ssh.exec_command(cmd1)
	sftp.mkdir(config_dir)
	file1=os.listdir("tmp")
	for i in file1: 
		local1='tmp/' + i
		remote1=config_dir + i
		print("upload file " + local1 + " to " + remote1)
		sftp.put(local1,remote1)
	sftp.close()
	ssh.close()

def get_gateway4(d1,i):
	vm_bridge = d1['vm'][i]['interfaces']['mgmt']['bridge']
	gateway4 = '0.0.0.0'
	for i in d1['vm']['gw']['interfaces'].keys():
		if d1['vm']['gw']['interfaces'][i]['bridge'] == vm_bridge:
			gateway4 = d1['vm']['gw']['interfaces'][i]['family']['inet'].split('/')[0]
	return gateway4

def create_junos_config(d1,i):
	dummy1={}
	dummy1['hostname']=i
	dummy1['username']=d1['junos_login']['login']
	dummy1['password']=md5_crypt.hash(d1['junos_login']['password'])
	dummy1['ssh_key']=d1['pod']['ssh_key_host']
	#print(f"VM is {i}")
	#dummy1['ntpserver']=d1['pod']['ntp']
	if d1['vm'][i]['os'] == 'vmx':
		dummy1['type']='vmx'
	# elif d1['vm'][i]['os'] == 'vqfx':
	# 	dummy1['type']='vqfx'
	elif d1['vm'][i]['os'] == 'vsrx':
		dummy1['type']='vsrx'
	# elif d1['vm'][i]['os'] == 'vrr':
	# 	dummy1['type']='vrr'
	elif d1['vm'][i]['os'] == 'vjunos_switch':
		dummy1['type']='vjunos_switch'
	elif d1['vm'][i]['os'] == 'vjunos_router':
		dummy1['type']='vjunos_router'
	# elif d1['vm'][i]['os'] == 'evo':
	# 	dummy1['type']='evo'
	elif d1['vm'][i]['os'] == 'vjunos_evolved':
		dummy1['type']='vjunos_evolved'
	elif d1['vm'][i]['os'] == 'vjunos_evolvedBX':
		dummy1['type']='vjunos_evolvedBX'
	# dummy1['gateway4']=d1['vm']['gw']['interfaces']['em1']['family']['inet'].split('/')[0]
	dummy1['gateway4'] = get_gateway4(d1,i)
	dummy1['mgmt_ip']=d1['vm'][i]['interfaces']['mgmt']['family']['inet']
	dummy1['interfaces']=None
	dummy1['protocols']=None
	#dummy1['static']=[]
	dummy1['rpm']={}
	# if 'ztp' in d1['vm'][i].keys():
	# 	if d1['vm'][i]['ztp']:
	# 		dummy1['mgmt_dhcp'] = 1
	# 	else: 
	# 		dummy1['mgmt_dhcp'] = 0
	# else:
	# 	dummy1['mgmt_dhcp'] = 0
	#print(f"vm {i}")
	if d1['vm'][i]['mgmt_dhcp']:
		dummy1['mgmt_dhcp'] = 1
	else:
		dummy1['mgmt_dhcp'] = 0
	if d1['vm'][i]['mgmt_instc']:
		dummy1['mgmt_instc'] = 1
	else:
		dummy1['mgmt_instc'] = 0
	# dummy1['mgmt_dhcp'] = 0
	# if 'mgmt_dhcp' in d1['vm'][i].keys():
	# 	if d1['vm'][i]['mgmt_dhcp']:
	# 		dummy1['mgmt_dhcp'] = 1
	# if 'mgmt_instc' in d1['vm'][i].keys():
	# 	if d1['vm'][i]['mgmt_instc']:
	# 		dummy1['mgmt_instc'] = 1
	# 	else: 
	# 		dummy1['mgmt_instc'] = 0
	# else:
	# 	dummy1['mgmt_instc'] = 1
	# if 	'router-id' in d1['vm'][i].keys():	
	# 	dummy1['router_id']  = d1['vm'][i]['router-id']
	if 'isis_dm' in d1.keys():
		if d1['isis_dm']:
			dummy1['isis_dm']=True
	if 'lo0' in d1['vm'][i]['interfaces'].keys():
		if 'family' in d1['vm'][i]['interfaces']['lo0'].keys():
			if 'inet' in d1['vm'][i]['interfaces']['lo0'].keys():
				dummy1['router_id']  = d1['vm'][i]['interfaces']['lo0']['inet'].split('/')[0]
	if 	'srv6-locator' in d1['vm'][i].keys():
		dummy1['srv6_locator'] = d1['vm'][i]['srv6-locator']
		dummy1['srv6_end_sid'] = d1['vm'][i]['srv6-locator'].split('/')[0]
	
	if 'snmp' in d1.keys():
		dummy1['snmp'] = { 'server' : d1['snmp']['server'],'ro_comm' : d1['snmp']['ro_community'] }
	if "lo0" in d1['vm'][i]['interfaces'].keys():
		if 'family' in d1['vm'][i]['interfaces']['lo0'].keys():
			if 'inet' in d1['vm'][i]['interfaces']['lo0']['family'].keys():
				dummy1['router_id']  = d1['vm'][i]['interfaces']['lo0']['family']['inet'].split('/')[0]
				if 'paragon_ingest' in d1.keys():
					dummy1['ingest']={'ip' : d1['paragon_ingest'],'source': d1['vm'][i]['interfaces']['lo0']['family']['inet'].split('/')[0]}
				if 'pcep' in d1['vm'][i].keys():
					if d1['vm'][i]['pcep']=='yes' or d1['vm'][i]['pcep']==True:
						if 'pcep_server' in d1.keys():
							dummy1['pcep']={'server': d1['pcep_server'],'local': d1['vm'][i]['interfaces']['lo0']['family']['inet'].split('/')[0] }
				if 'bgpls' in d1['vm'][i].keys():
					dummy1['bgpls']={'as' : d1['vm'][i]['bgpls']['as'],'local' : d1['vm'][i]['interfaces']['lo0']['family']['inet'].split('/')[0]}
	for j in d1['vm'][i]['interfaces'].keys():
		if j != 'mgmt':
			if j[0:2] not in  [ 'em','vi']:
				#if 'mtu' in  d1['vm'][i]['interfaces'][j].keys():
				#	add_mtu(dummy1,j,d1['vm'][i]['interfaces'][j]['mtu'])
				#add_into_protocols(dummy1,'lldp',j,"")
				if 'mtu' in d1['vm'][i]['interfaces'][j].keys():
					add_mtu(dummy1,j,d1['vm'][i]['interfaces'][j]['mtu'])
				if 'family' in d1['vm'][i]['interfaces'][j].keys():
					if 'mpls' in d1['vm'][i]['interfaces'][j]['family'].keys():
						add_into_protocols(dummy1,'mpls',j,"")
					for k in d1['vm'][i]['interfaces'][j]['family'].keys():
						if d1['vm'][i]['interfaces'][j]['family'][k]:
							add_into_interfaces(dummy1,j,k,d1['vm'][i]['interfaces'][j]['family'][k])
						else:
							add_into_interfaces(dummy1,j,k,True)
				if 'protocol' in d1['vm'][i]['interfaces'][j].keys():
					#print("protocol found")
					for k in d1['vm'][i]['interfaces'][j]['protocol'].keys():
						if k == 'mpls':
							pass
						elif k == 'isis':
							if d1['vm'][i]['interfaces'][j]['protocol'][k] == 'ptp':
								option = 'point-to-point'
							elif d1['vm'][i]['interfaces'][j]['protocol'][k] == 'passive':
								option = 'passive'
							else:
								option = ""
						else:
							option = ""
						#print("interface %s protocol %s option %s" %(j,k,option))
						add_into_protocols(dummy1,k,j,option)
				if 'rpm' in d1['vm'][i]['interfaces'][j].keys():
					intf = j + ".0"
					src = d1['vm'][i]['interfaces'][j]['rpm']['source']
					dst = d1['vm'][i]['interfaces'][j]['rpm']['destination']
					dummy1['rpm'].update({intf : { 'src': src, 'dst': dst }})
				if 'desc' in d1['vm'][i]['interfaces'][j].keys():
					add_desc(dummy1,j,d1['vm'][i]['interfaces'][j]['desc'])
				#if 'static' in d1['vm'][i]['interfaces'][j].keys():
				#	for k in d1['vm'][i]['interfaces'][j]['static']:
				#		d1['vm'][i]['interfaces'][j]['static'].append(
				#			{'to': k['to'], 'via':k['via']}
				#		)
				#	add_into_route_options_static(dummy1,)
	#pprint.pprint(dummy1)
	return dummy1


def write_junos_config(d1):
	data1=[]
	print("Junos config write")
	#ssh_key = read_ssh_key(d1)
	#print("ssh key ",ssh_key)
	try:
		#print("template ",param1.junos_template)
		with open(d1['template']['junos']) as f1:
			jt=f1.read()
		# with open(d1['template']['junos2']) as f1:
		# 	jt2=f1.read()
		# with open(d1['template']['junos3']) as f1:
		# 	jt3=f1.read()
		# f1=open(d1['pod']['path'] + param1.junos_template)
		#f1.close()
		for i in d1['vm'].keys():
			if d1['vm'][i]['type'] in param1.junos_type:
				dummy1 = create_junos_config(d1,i)
				# if 'dhcp' in d1['vm'][i].keys():
				# 	if d1['vm'][i]['dhcp'] == 2:
				# 		config1=Template(jt2).render(dummy1)
				# 	elif d1['vm'][i]['dhcp'] == 3:
				# 		config1=Template(jt3).render(dummy1)
				# 	else:
				# 		config1=Template(jt).render(dummy1)
				# else:
				# 	# print(f"template junos static {i} ")
				#   config1=Template(jt).render(dummy1)
				config1=Template(jt).render(dummy1)
				f1=param1.tmp_dir + i + ".conf"
				with open(f1,"w") as wr1:
					wr1.write(config1)
				#write_to_file_config(f1,config1)
	except PermissionError:
		print("permission error")

def add_mtu(dt,intf,mtu):
	if not dt['interfaces']:
		dt['interfaces']={intf:None}
	if intf not in dt['interfaces'].keys():
		dt['interfaces'][intf]=None
	dt['interfaces'][intf]={'mtu':mtu}
	#return dt

def add_desc(dt,intf,desc):
	if not dt['interfaces']:
		dt['interfaces']={intf:None}
	if intf not in dt['interfaces'].keys():
		dt['interfaces'][intf]=None
	if 'desc' not in dt['interfaces'][intf].keys():
		dt['interfaces'][intf]['desc']=desc

def add_into_interfaces(dt,intf,family,family_address):
	if not dt['interfaces']:
		dt['interfaces']={intf:None}
	if intf not in dt['interfaces'].keys():
		dt['interfaces'][intf]=None
	if not dt['interfaces'][intf]:
		dt['interfaces'][intf]={family:None}
	if family not in dt['interfaces'].keys():
		dt['interfaces'][intf][family]=family_address
	#return dt

def add_into_protocols(dt,prot,intf,option):
	if not dt['protocols']:
		dt['protocols']={prot:None}
	if prot not in dt['protocols'].keys():
		dt['protocols'][prot]=None
	if not dt['protocols'][prot]:
		dt['protocols'][prot]={intf:None}
	if intf not in dt['protocols'][prot].keys():
		dt['protocols'][prot][intf]=None
	if option:
		dt['protocols'][prot][intf]=option
	#return dt

def prefix2netmask(prefs):
	i=0
	b=[]
	pref = int(prefs)
	for i in range(4):
		# print("pref ",pref)
		if pref >= 8:
			b.append(255)
		elif pref >= 0:
			b1=0
			f1=7
			for j in list(range(pref)):
				b1 +=  2 ** f1
				f1 -= 1
			b.append(b1)
		else:
			b.append(0)
		pref -= 8
	return str(b[0]) + "." + str(b[1]) + "." + str(b[2]) + "." + str(b[3])

def netmask2prefix(netmask):
    b = netmask.split('.')
    prefix = 0
    for i in b:
        t = int(i)
        match t:
            case 0b11111111:
                l = 8
            case 0b11111110:
                l = 7
            case 0b11111100:
                l = 6
            case 0b11111000:
                l = 5
            case 0b11110000:
                l = 4
            case 0b11100000:
                l = 3
            case 0b11000000:
                l = 2
            case 0b10000000:
                l = 1
            case 0b0:
                l = 0
        prefix += l
    return prefix

def write_to_file(f1,line1):
	print("writing " + f1)
	try:
		of=open(f1,"w")
		for i in line1:
			of.write(i + "\n")
		of.close()
	except PermissionError:
		print("permission error")

def write_to_file_config(f1,config):
	print("writing " + f1)
	try:
		of=open(f1,"w")
		of.write(config)
		of.close()
	except PermissionError:
		print("permission error")

def list_bridge(d1):
	vm_list=list(d1['vm'].keys())
	bridge1=[]
	for i in vm_list:
		print("host ",i)
		for j in d1['vm'][i]['interfaces'].keys():
			if j not in ["lo0","irb"]:
				if d1['vm'][i]['interfaces'][j]['bridge'] not in bridge1:
					bridge1.append(d1['vm'][i]['interfaces'][j]['bridge'])
	return bridge1

def list_of_bridge(d1):
	vm_list=list(d1['vm'].keys())
	#retval=[]
	bridge1=[]
	for i in vm_list:
		#print("host ",i)
		for j in d1['vm'][i]['interfaces'].keys():
			if j not in ["lo0","irb"]:
				#print(f"interface {j}")
				#print(d1['vm'][i]['interfaces'][j])
				#print(f" host {i} interface {j}")
				if d1['vm'][i]['interfaces'][j]['bridge'] != 'external': 
					if d1['vm'][i]['interfaces'][j]['bridge'] not in bridge1:
						bridge1.append(d1['vm'][i]['interfaces'][j]['bridge'])
	return bridge1

def list_bridge_for_vmm(d1):
	vm_list=list(d1['vm'].keys())
	retval=[]
	bridge1=[]
	for i in vm_list:
		#print("host ",i)
		for j in d1['vm'][i]['interfaces'].keys():
			if j not in ["lo0","irb"]:
				#print(f"interface {j}")
				#print(d1['vm'][i]['interfaces'][j])
				if d1['vm'][i]['interfaces'][j]['bridge'] != 'external': 
					if d1['vm'][i]['interfaces'][j]['bridge'] not in bridge1:
						bridge1.append(d1['vm'][i]['interfaces'][j]['bridge'])
	for i in bridge1:
		retval.append('  bridge "' + i + '"{};')
	retval.append('  bridge "reserved_bridge"{};')
	for i in d1['vm'].keys():
		if d1['vm'][i]['os']=='vqfx':
			retval.append('  bridge "' + i + 'INT"{};')
	retval.append('  PRIVATE_BRIDGES')
	return retval

def get_bridge_name(intf):
	if isinstance(intf,list):
		return intf[0]
	elif isinstance(intf,str):
		return intf

def change_intf(intf):
	return intf.replace('em','eth')
# def change_intfx(intf):
#	return intf.replace('em','ens3f')

# def make_config_generic_pc(d1,i):
# 	retval=[]
# 	#config_dir=param1.home_dir + d1['pod']['user'] + '/' + d1['name'] + "/"
# 	config_dir=d1['pod']['home_dir'] + '/vm/' + d1['name'] + "/"
# 	# print("Make config for GW for vm ",i)
# 	retval.append('vm "'+i+'" {')
# 	retval.append('   hostname "'+i+'";')
# 	if 'disk' in d1['vm'][i].keys():
# 		temp_s1="    " + d1['vm'][i]['os'].upper() + "_" + d1['vm'][i]['disk'].upper() +  "_DISK"
# 	else:
# 		temp_s1="    " + d1['vm'][i]['os'].upper() +  "_DISK"
# 	retval.append(temp_s1)
# 	if 'hd2' in d1['vm'][i].keys():
# 		# disk "hdb" "/vmm/data/user_disks/irzan/vm/vmware/esxi3disk2.vmdk";
# 		retval.append(f"     disk \"hdb\" \"{config_dir}{i}-disk2.img\";")
# 	if d1['vm'][i]['type'] in ['pchpv1','pchpv2','ssrr']:
# 		retval.append('   setvar "+qemu_args" "-cpu host,+vmx";')
# 	else:
# 		retval.append('   setvar "+qemu_args" "-cpu qemu64,+vmx";')
# 	retval.append('   ncpus ' + str(param1.vm_type[d1['vm'][i]['type']]['ncpus']) + ';')
# 	retval.append('   memory ' + str(param1.vm_type[d1['vm'][i]['type']]['memory']) + ';')
# 	if 'vnc' in d1['vm'][i]:
# 		if (d1['vm'][i]['vnc']):
# 			retval.append('   setvar "enable_vnc" "1";')
# 	for j in d1['vm'][i]['interfaces'].keys():
# 		# if d1['vm'][i]['os'] == 'ssr':
# 		# 	intf = j.replace('em','vio')
# 		# else:
# 		# 	intf = j
# 		intf = j
# 		retval.append('   interface "' +  intf + '" { bridge "' + d1['vm'][i]['interfaces'][j]['bridge'] + '";};')
# 	return retval

# def init_junos(d1,vm=""):
# 	print("this is for init junos")
# 	list_of_jvm=[]
# 	for i in d1['vm'].keys():
# 		if d1['vm'][i]['os'] in ['vjunos_switch','evo','vjunos-router','vjunos_evolved','vjunos_evolvedBX']:
# 			list_of_jvm.append(i)
# 	if list_of_jvm:
# 		if vm:
# 			#print(f"VM is {vm}")
# 			if vm not in list_of_jvm:
# 				print(f"VM {vm} is not configured in this topology")
# 			else:
# 				send_init(d1,vm)
# 				# config_junos(d1,vm)
# 		else:
# 			print("list of virtual junos ",list_of_jvm)
# 			for i in list_of_jvm:
# 				send_init(d1,i)
# 			# config_junos(d1)

# def init_vjunos(d1,vm=""):
# 	print("this is for init vjunos")
# 	list_of_jvm=[]
# 	for i in d1['vm'].keys():
# 		if d1['vm'][i]['os'] in  ['vjunos_switch','vjunos_router']:
# 			list_of_jvm.append(i)
# 	if list_of_jvm:
# 		if vm:
# 			#print(f"VM is {vm}")
# 			if vm not in list_of_jvm:
# 				print(f"VM {vm} is not configured in this topology")
# 			else:
# 				send_init_vjunos(d1,vm)
# 				# config_junos(d1,vm)
# 		else:
# 			print("list of virtual junos ",list_of_jvm)
# 			for i in list_of_jvm:
# 				send_init_vjunos(d1,i)
# 			# config_junos(d1)


def connect_to_vm(d1,i):
	ssh_gw = connect_to_gw(d1)
	host_ip = get_mgmt_ip(d1,i)
	user_id, passwd = get_user(d1,i)
	jumphost_transport=ssh_gw.get_transport()
	src_addr=(d1['gw_ip'],22)
	if d1['vm'][i]['type']in ['junos','vjunos_router','vjunos_switch']:
		dest_addr=(d1['vm'][i]['interfaces']['mgmt']['family']['inet'].split('/')[0],22)
	else:
		dest_addr=(d1['vm'][i]['interfaces']['em0']['family']['inet'].split('/')[0],22)
	#print(f"source address {src_addr[0]}, destination address {dest_addr[0]}")
	jumphost_channel = jumphost_transport.open_channel("direct-tcpip", dest_addr, src_addr)
	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# ssh.connect(hostname=d1['pod']['vmmserver'],username=d1['pod']['user'],password=d1['pod']['unixpassword'],sock=jumphost_channel)
	ssh.connect(hostname=host_ip,username=user_id,password=passwd,sock=jumphost_channel)
	return ssh

# def config_junos(d1,vm=""):
# 	if not vm:
# 		print("this is put configuration into vEX and vEVO")
# 		list_of_jvm=[]
# 		for i in d1['vm'].keys():
# 			if d1['vm'][i]['os'] in ['vjunos_switch','evo','vjunos_router','vjunos_evolved','vjunos_evolvedBX']:
# 				list_of_jvm.append(i)
# 		if list_of_jvm:
# 			print("list of virtual junos ",list_of_jvm)
# 			#d1['gw_ip']=get_ip_vm(d1,'gw')
# 			for i in list_of_jvm:
# 				#print(f"To vm {i}")
# 				upload_to_vm(d1,i)
# 	else:
# 		upload_to_vm(d1,vm)

# def upload_to_vm(d1,i):
# 	local1 = f"./tmp/{i}.conf"
# 	remote1= f"~/{i}.conf"
# 	print(f"uploading file {local1} to {i}")
# 	ssh2host=connect_to_vm(d1,i)
# 	scp = SCPClient(ssh2host.get_transport())
# 	scp.put(local1,remote1)
# 	scp.close()
# 	cmd1 = f"edit ; load merge relative {i}.conf ; commit"
# 	print(f"executing {cmd1}")
# 	s1,s2,s3=ssh2host.exec_command(cmd1)
# 	for i in s2.readlines():
# 		print(i)
# 	ssh2host.close()

# def send_init(d1,i):
# 	status=0
# 	my_hash_root = md5_crypt.hash(d1['junos_login']['password'])
# 	my_hash = md5_crypt.hash(d1['junos_login']['password'])
# 	#cmd1="vmm serial -t " + i
# 	ip_mgmt = d1['vm'][i]['interfaces']['mgmt']['family']['inet']
# 	#br_mgmt = d1['vm'][i]['interfaces']['mgmt']['bridge']
# 	if 'gateway4' not in d1['vm'][i]['interfaces']['mgmt']['family']:
# 		gateway4 = '0.0.0.0'
# 	else:
# 		gateway4 = d1['vm'][i]['interfaces']['mgmt']['family']['gateway4']
# 	#gateway4 = get_gateway4(d1,i)
# 	junos_status=0
# 	print("configuring ",i)
# 	if d1['vm'][i]['os'] in  ['vjunos_switch']:
# 		junos_status=1
# 		c1=f"ssh vmm 'vmm serial -t {i}'"
# 		print(f"COMMAND {c1}")
# 		s_e = [
# 				["","login:"],
# 				["root","root@"],
# 				["cli","root>"],
# 				["configure","root#"],
# 				["delete interfaces fxp0","root#"],
# 				["delete chassis","root#"],
# 				["delete protocols","root#"],
# 				["delete system processes dhcp-service","root#"],
# 				["set system host-name " + i,"root#"],
# 				[f"set system root-authentication encrypted-password \"{my_hash_root}\"","root#"],
# 				["set system services ssh","root#"],
# 				["set system services netconf ssh","root#"],
# 				[f"set system login user {d1['junos_login']['login']} class super-user authentication encrypted-password \"{my_hash}\"","root#"],
# 				[f"set interfaces fxp0 unit 0 family inet address {ip_mgmt}","root#"],
# 				["set system management-instance","root#"],
# 				[f"set routing-instances mgmt_junos routing-options static route 0.0.0.0/0 next-hop {gateway4}", "root#"],
# 				["set chassis network-services enhanced-ip","root#"],
# 				["set chassis evpn-vxlan-default-switch-support","root#"],
# 				["set snmp community public authorization read-only","root#"],
# 				["commit",f"root@{i}#"],
# 				["exit",f"root@{i}>"],
# 				["request system reboot","(no)"],
# 				["yes","IMMEDIATELY"]	
# 			] 
# 				# ["exit","root@:~ #"],
# 				# ["exit","login:"]
# 			## [f"set system login user {d1['junos_login']['login']} authentication ssh-rsa \"{d1['pod']['ssh_key']}\"","root#"],
# 	elif d1['vm'][i]['os'] in  ['evo','vjunos_evolved','vjunos_evolvedBX']:
# 		junos_status=1
# 		if d1['vm'][i]['os'] == 'evo':
# 			c1=f"ssh vmm 'vmm serial -t {i}_RE0'"
# 		elif d1['vm'][i]['os'] == 'vjunos_evolved' or d1['vm'][i]['os'] == 'vjunos_evolvedBX':
# 			c1=f"ssh vmm 'vmm serial -t {i}'"
# 		print(f"COMMAND {c1}")
# 		s_e = [
# 				["","login:"],
# 				["root","root@re0:~#"],
# 				["cli","root@re0>"],
# 				["configure","root@re0#"],
# 				["delete system commit","root@re0#"],
# 				["delete chassis","root@re0#"],
# 				["set system host-name " + i,"root@re0#"],
# 				[f"set system root-authentication encrypted-password \"{my_hash_root}\"","root@re0#"],
# 				["set system services ssh","root@re0#"],
# 				["set system services netconf ssh","root@re0#"],
# 				[f"set system login user {d1['junos_login']['login']} class super-user authentication encrypted-password \"{my_hash}\"","root@re0#"],
# 				[f"set interfaces re0:mgmt-0 unit 0 family inet address {ip_mgmt}","root@re0#"],
# 				["set system management-instance","root@re0#"],
# 				[f"set routing-instances mgmt_junos routing-options static route 0.0.0.0/0 next-hop {gateway4}", "root@re0#"],
# 				["set snmp community public authorization read-only","root@re0#"],
# 				[f"commit",f"root@{i}#"],
# 				[f"exit",f"root@{i}>"],
# 				["exit","root@re0:~#"],
# 				["exit","login:"]
# 			]
# 			## [f"set system login user {d1['junos_login']['login']} authentication ssh-rsa \"{d1['pod']['ssh_key']}\"","root@re0#"],
# 	if junos_status:
# 		p1=pexpect.spawn(c1)
# 		for j in s_e:
# 			print(f"send :{j[0]}")
# 			p1.sendline(j[0])
# 			print(f"expect : {j[1]}")
# 			p1.expect(j[1], timeout=240)
# 		p1.close()

# def send_init_vjunos(d1,i):
# 	status=0
# 	my_hash_root = md5_crypt.hash(d1['junos_login']['password'])
# 	my_hash = md5_crypt.hash(d1['junos_login']['password'])
# 	#cmd1="vmm serial -t " + i
# 	#ip_mgmt = d1['vm'][i]['interfaces']['mgmt']['family']['inet']
# 	#br_mgmt = d1['vm'][i]['interfaces']['mgmt']['bridge']
# 	#if 'gateway4' not in d1['vm'][i]['interfaces']['mgmt']['family']:
# 	#	gateway4 = '0.0.0.0'
# 	#else:
# 	#	gateway4 = d1['vm'][i]['interfaces']['mgmt']['family']['gateway4']
# 	#gateway4 = get_gateway4(d1,i)
# 	junos_status=0
# 	print("configuring ",i)
# 	if d1['vm'][i]['os'] in  ['vjunos_switch']:
# 		junos_status=1
# 		c1=f"ssh vmm 'vmm serial -t {i}'"
# 		ip_mgmt = d1['vm'][i]['interfaces']['mgmt']['family']['inet']
# 		print(f"COMMAND {c1}")
# 		s_e = [
# 				["","login:"],
# 				["root","root@"],
# 				["cli","root>"],
# 				["configure","root#"],
# 				["delete interfaces fxp0","root#"],
# 				["delete chassis","root#"],
# 				["delete protocols","root#"],
# 				["delete system processes dhcp-service","root#"],
# 				["set system host-name " + i,"root#"],
# 				[f"set system root-authentication encrypted-password \"{my_hash_root}\"","root#"],
# 				["set system services ssh","root#"],
# 				["set system services netconf ssh","root#"],
# 				[f"set system login user {d1['junos_login']['login']} class super-user authentication encrypted-password \"{my_hash}\"","root#"],
# 				[f"set interfaces fxp0 unit 0 family inet address {ip_mgmt}","root#"],
# 				["set chassis network-services enhanced-ip","root#"],
# 				["set chassis evpn-vxlan-default-switch-support","root#"],
# 				["set snmp community public authorization read-only","root#"],
# 				["commit",f"root@{i}#"],
# 				["exit",f"root@{i}>"],
# 				["request system reboot","(no)"],
# 				["yes","IMMEDIATELY"]	
# 			] 
# 	if d1['vm'][i]['os'] in  ['vjunos_router']:
# 		junos_status=1
# 		ip_mgmt = d1['vm'][i]['interfaces']['mgmt']['family']['inet']
# 		c1=f"ssh vmm 'vmm serial -t {i}'"
# 		print(f"COMMAND {c1}")
# 		s_e = [
# 				["","login:"],
# 				["root","root@"],
# 				["cli","root>"],
# 				["configure","root#"],
# 				["delete interfaces fxp0","root#"],
# 				["delete chassis","root#"],
# 				["delete protocols","root#"],
# 				["delete system processes dhcp-service","root#"],
# 				["set system host-name " + i,"root#"],
# 				[f"set system root-authentication encrypted-password \"{my_hash_root}\"","root#"],
# 				["set system services ssh","root#"],
# 				["set system services netconf ssh","root#"],
# 				[f"set system login user {d1['junos_login']['login']} class super-user authentication encrypted-password \"{my_hash}\"","root#"],
# 				[f"set interfaces fxp0 unit 0 family inet address {ip_mgmt}","root#"],
# 				["set chassis network-services enhanced-ip","root#"],
# 				["set snmp community public authorization read-only","root#"],
# 				["commit",f"root@{i}#"],
# 				["exit",f"root@{i}>"],
# 				["request system reboot","(no)"],
# 				["yes","IMMEDIATELY"]	
# 			]
# 	if junos_status:
# 		p1=pexpect.spawn(c1)
# 		for j in s_e:
# 			print(f"send :{j[0]}")
# 			p1.sendline(j[0])
# 			print(f"expect : {j[1]}")
# 			p1.expect(j[1], timeout=240)
# 		p1.close()
