#!/usr/bin/env python3
home_dir='/vmm/data/user_disks/'
kvm_dir='/disk2/vm/'
pc_type=['gw','pctiny','pcsmall','pcmedium','pcbig','pcxbig','pchpv0','pchpv1','pchpv2','pchpv3','bridge','cpe','paagent','ssrc','ssrr','aos','aos_ztp']
junos_template='junos.j2'
junos_type=['vsrx','vmx','mx240','mx480','mx960','vjunos_switch','vjunos_router','vjunos_evolved','vjunos_evolvedBX']
# vm_type_old={
#    'gw': {'ncpus' : 2,'memory':4096},
#    'paagent': {'ncpus' : 1,'memory':1024},
#    'pctiny': {'ncpus' : 1,'memory':4096},
#    'pcsmall': {'ncpus' : 2,'memory':8192},
#    'pcmedium': {'ncpus' : 2,'memory':16384},
#    'pcbig': {'ncpus' : 4,'memory':32768},
#    'pchpv1': {'ncpus' : 8,'memory':32768},
#    'pchpv2': {'ncpus' : 8,'memory':16384},
#    'pcxbig': {'ncpus' : 8,'memory':65536},
#    'esxi': {'ncpus' : 8,'memory':32768},
#    'vcsa': {'ncpus' : 4,'memory':16384},
#    'vapp': {'ncpus' : 4,'memory':32768},
#    'vapp_s': {'ncpus' : 1,'memory':4096},
#    'ssrc': {'ncpus' : 4,'memory':16384},
#    'ssrr': {'ncpus' : 4,'memory':8192},
#    'junos': '',
#    'vspirent': {'ncpus' : 2,'memory':1024},
#    'bridge': {'ncpus' : 2,'memory':2048},
#    'cpe': {'ncpus' : 1,'memory':256},
#    'veos': {'ncpus' : 2, 'memory':4096}
# }
vm_type={
   'gw': {'ncpus' : 2,'memory':4096,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'pctiny': {'ncpus' : 1,'memory':4096,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'pcsmall': {'ncpus' : 2,'memory':8192,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'pcmedium': {'ncpus' : 4,'memory':16384,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'pcbig': {'ncpus' : 4,'memory':32768,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'pchpv0': {'ncpus' : 16,'memory':32768,'setvar':'"+qemu_args" "-cpu host,+vmx"'},
   'pchpv1': {'ncpus' : 8,'memory':32768,'setvar':'"+qemu_args" "-cpu host,+vmx"'},
   'pchpv2': {'ncpus' : 4,'memory':16384,'setvar':'"+qemu_args" "-cpu host,+vmx"'},
   'pchpv3': {'ncpus' : 8,'memory':65536,'setvar':'"+qemu_args" "-cpu host,+vmx"'},
   'pcxbig': {'ncpus' : 8,'memory':65536,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'vapp': {'ncpus' : 4,'memory':32768,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'vapp_s': {'ncpus' : 1,'memory':4096,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'ssrc': {'ncpus' : 4,'memory':16384,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'ssrr': {'ncpus' : 4,'memory':8192,'setvar':'"+qemu_args" "-cpu host,+vmx"'},
   'paagent': {'ncpus' : 1,'memory':1024,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'vspirent': {'ncpus' : 2,'memory':1024,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'bridge': {'ncpus' : 2,'memory':2048,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'cpe': {'ncpus' : 1,'memory':1024,'setvar':'"+qemu_args" "-cpu qemu64,+vmx"'},
   'vjunos_switch' : {'ncpus' : 4,'memory':5120,'setvar':'"+qemu_args" "-cpu host,+vmx -smbios type=1,product=VM-VEX"'},
   'vjunos_router_old' : {'ncpus' : 4,'memory':5120,'setvar':'"+qemu_args" "-cpu host,+vmx -smbios type=1,product=VM-VMX,family=lab"'},
   'vjunos_router' : {'ncpus' : 4,'memory':5120,'setvar':'"+qemu_args" "-cpu host,+vmx"'},
   'vjunos_evolved': {'ncpus' : 4,'memory':8192,'setvar':'"+qemu_args" "-cpu host,+vmx -smbios type=0,vendor=Bochs,version=Bochs -smbios type=3,manufacturer=Bochs -smbios type=1,manufacturer=Bochs,product=Bochs,serial=chassis_no=0:slot=0:type=1:assembly_id=0x0D20:platform=251:master=0:channelized=no"'},
   'vjunos_evolvedBX': {'ncpus' : 4,'memory':8192,'setvar':'"+qemu_args" "-cpu host,+vmx -smbios type=0,vendor=Bochs,version=Bochs -smbios type=3,manufacturer=Bochs -smbios type=1,manufacturer=Bochs,product=Bochs,serial=chassis_no=0:slot=0:type=1:assembly_id=0x0DA9:platform=272:master=0:channelized=no"'},
   'vsrx': {'ncpus' : 2,'memory':4096,'setvar':'"qemu_args" "-cpu qemu64,+vmx,+ssse3,+sse4_1,+sse4_2,+aes,+avx,+pat,+pclmulqdq,+rdtscp,+syscall,+tsc-deadline,+x2apic,+xsave"'},
   'vmx' : {'i2cid': 161}, 
   'mx240' : {'i2cid': 48}, 
   'mx480' : {'i2cid': 33}, 
   'mx960' : {'i2cid': 21}
}
pc_type_only = [ x for x in vm_type.keys() if 'pc' in x]
vjunos_type = set([ x for x in vm_type.keys() if 'vjunos' in x])
# print(pc_type)
# vm_os=['centos','ubuntu','vmx','vqfx','vsrx','evo','mx960','mx480','mx240','wrt']
# vm_os=['gw','alpine','centos','rhel','ubuntu','ubuntu2','debian','desktop','vmx','jspace','sdi','pa2',
#        'vsrx','vjunos_switch','vjunos_router','vjunos_evolved','vjunos_evolvedBX','wrt','aos','aos_ztp','aos_flow','bridge','paagent','ssr']
tmp_dir="./tmp/"
vmm_group="vmm-default"
esxi_ds_size=100
#vmm_servers = ["q-pod05", "q-pod08","q-pod13", "q-pod21", "q-pod22", "q-pod23", "q-pod25", "q-pod26", "q-pod27", "q-pod29", "q-pod30", "q-pod32", "q-pod35","q-pod36","q-pod38","q-pod39","elpod1", "elpod2", "elpod3", "enpod2", "enpod4", "enpod6", "enpod7"]
# vmm_servers = ["q-pod08","q-pod13", "q-pod21", "q-pod22", "q-pod23", "q-pod25", "q-pod26", "q-pod27", "q-pod29", "q-pod30", "q-pod32", "q-pod35","q-pod36","q-pod38"]

# jnpr_dns1="66.129.233.81"
# jnpr_dns2="66.129.233.82"
jnpr_dns = ['10.49.32.95','10.49.32.97']
# #jnpr_dns1="8.8.8.8"
# #jnpr_dns2="8.8.4.4"

# config for topology
# bit 0 : ipv4
# bit 1 : ipv6
# bit 2 : iso
# bit 3 : mpls
# bit 4 : isis
# bit 5 : rsvp
# bit 6 : ldp
# bit 7 : delay measurement using RPM
# bit 8 : large mtu
mask_ipv4 = 0b1
mask_ipv6 = 0b10
mask_iso  = 0b100
mask_mpls = 0b1000
mask_isis = 0b10000
mask_rsvp = 0b100000
mask_ldp  = 0b1000000
mask_rpm  = 0b10000000
mask_mtu  = 0b100000000
mtu= 9000

