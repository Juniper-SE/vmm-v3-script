#!/bin/bash
VM=vm1
DISK=${VM}.img
VLAN=401
LAN=ovs1
virt-install --name ${VM} \
  --disk /vm/${DISK},device=disk,bus=virtio \
  --disk /vm/seed.iso,device=cdrom \
  --ram 4096 --vcpu 1 --osinfo debian12 \
  --network=bridge:${LAN},model=virtio,virtualport_type=openvswitch \
  --xml "./devices/interface/vlan/tag/@id=${VLAN}" \
  --xml "./devices/interface/target/@dev=${VM}_e0" \
  --console pty,target_type=serial \
  --noautoconsole \
  --vnc \
  --virt-type=qemu \
  --boot hd --noreboot
