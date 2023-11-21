#!/usr/bin/env python3
import sys
import os
import lib1
import time
# yaml.warnings({'YAMLLoadWarning': False})
time_start = time.time()
config1=lib1.check_argv(sys.argv)
if config1:
	# print("configuration ",config1)
	d1=lib1.read_config(config1)
	#print(d1)
	#d1={}
	#print(f"config {config1['cmd']} {config1['vm']}")
	#print(d1['template'])
	if d1:
		if config1['cmd'] == 'upload':
			lib1.upload(d1)
		elif config1['cmd'] == 'config':
			lib1.upload(d1,0)
		elif config1['cmd'] == 'start':
			lib1.start(d1)
		elif config1['cmd'] == 'lsbr':
			lsbr=lib1.list_bridge(d1)
			print(lsbr)
		elif config1['cmd'] == 'stop':
			print('stop topology on vmm')
			lib1.stop(d1)
		elif config1['cmd'] == 'list':
			lib1.list_vm(d1)
		elif config1['cmd'] == 'set_gw':
			lib1.set_gw(d1)
		elif config1['cmd'] == 'set_host':
			lib1.set_host(d1,config1['vm'])
		elif config1['cmd'] == 'test':
			lib1.test(d1)
		elif config1['cmd'] == 'ssh_config':
			lib1.write_ssh_config(d1)
		elif config1['cmd'] == 'init_junos':
			lib1.init_junos(d1,config1['vm'])
		elif config1['cmd'] == 'init_vjunos':
			lib1.init_vjunos(d1)
		elif config1['cmd'] == 'config_junos':
			lib1.config_junos(d1)
		elif config1['cmd'] == 'get_ztp_config':
			lib1.get_ztp_config(d1)
		# elif config1['cmd'] == 'get_vjunos_dhcp':
		# 	lib1.get_vjunos_config(d1)
		elif config1['cmd'] == 'print_data':
			lib1.print_data(d1)
		elif config1['cmd'] == 'change_dhcp':
			lib1.change_dhcp(d1)
		elif config1['cmd'] == 'get_vnc_list':
			lib1.get_vnc_list(d1)
		elif config1['cmd'] == 'get1':
			lib1.create_novnc(d1)
		# elif config1['cmd'] == 'get_dns':
		# 	lib1.get_dns(d1)
		#elif config1['cmd'] == 'get_serial':
		#	lib1.get_serial(d1,config1['vm'])
		#elif config1['cmd'] == 'get_vga':
		#	lib1.get_vga(d1,config1['vm'])
		#elif config1['cmd'] == 'get_ip':
		#	lib1.get_ip(d1,config1['vm'])
		else:
			print("wrong argument")
	else:
		print("data is not available")
	time_end=time.time()
	print("script run for %d seconds" %(time_end-time_start))
else:
	pass
