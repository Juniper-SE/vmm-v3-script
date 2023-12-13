#!/bin/bash
VM=svr1
DISK=${VM}.img
VLAN=100
LAN=ovsdc0
virt-install --name ${VM} \
  --disk ./${DISK},device=disk,bus=virtio \
  --disk ./seed.iso,device=cdrom \
  --ram 2048 --vcpu 1 --osinfo alpinelinux3.18 \
  --network=bridge:${LAN},model=virtio,virtualport_type=openvswitch \
  --xml "./devices/interface/vlan/tag/@id=${VLAN}" \
  --xml "./devices/interface/target/@dev=${VM}_e0" \
  --console pty,target_type=serial \
  --noautoconsole \
  --hvm --accelerate \
  --vnc \
  --virt-type=kvm \
  --boot hd --noreboot
