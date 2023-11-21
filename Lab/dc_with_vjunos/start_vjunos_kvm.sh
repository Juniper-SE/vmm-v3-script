#!/bin/bash
VM=sw1
DISK=${VM}.img
RAM=5120
VCPU=4
virt-install --name ${VM} \
	--disk ${DISK},device=disk \
	--ram ${RAM} --vcpu ${VCPU}  \
	--cpu SandyBridge-IBRS,+vmx \
	--sysinfo smbios,system_product=VM-VEX \
	--osinfo ubuntu22.04 \
	--network bridge=br0,virtualport_type=openvswitch \
	--network bridge=link0 \
	--network bridge=link1 \
	--network bridge=link2 \
	--network bridge=link3 \
	--xml './devices/interface[1]/target/@dev=sw1fxp0' \
	--xml './devices/interface[1]/vlan/tag/@id=101' \
	--xml './devices/interface[2]/target/@dev=sw1ge0' \
	--xml './devices/interface[2]/mtu/@size=9500' \
	--xml './devices/interface[3]/target/@dev=sw1ge1' \
	--xml './devices/interface[3]/mtu/@size=9500' \
	--xml './devices/interface[4]/target/@dev=sw1ge2' \
	--xml './devices/interface[4]/mtu/@size=9500' \
	--xml './devices/interface[5]/target/@dev=sw1ge3' \
	--xml './devices/interface[5]/mtu/@size=9500' \
	--console pty,target_type=serial \
	--noautoconsole \
	--hvm --accelerate  \
	--vnc  \
	--virt-type=kvm  \
	--boot hd