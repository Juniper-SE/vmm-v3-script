#!/bin/bash
VM=vm1
DISK=${VM}.img
VLAN=401
LAN=ovs1
virt-install --name ${VM} \
  --disk ./${DISK},device=disk,bus=virtio \
  --disk ./seed.iso,device=cdrom \
  --ram 2048 --vcpu 1 --osinfo debian11 \
  --network=bridge:${LAN},model=virtio,virtualport_type=openvswitch \
  --xml "./devices/interface/vlan/tag/@id=${VLAN}" \
  --xml "./devices/interface/target/@dev=${VM}_e0" \
  --console pty,target_type=serial \
  --noautoconsole \
  --hvm --accelerate \
  --vnc \
  --virt-type=kvm \
  --boot hd --noreboot --import



#!/bin/bash
VM=dhcp1
DISK=${VM}.img
VLAN=401
LAN=ovs0
virt-install --name ${VM} \
  --disk ./${DISK},device=disk,bus=virtio \
  --disk ./seed.iso,device=cdrom \
  --ram 2048 --vcpu 1 --osinfo ubuntu22.04 \
  --network=bridge:${LAN},model=virtio,virtualport_type=openvswitch \
  --xml "./devices/interface/target/@dev=${VM}_e0" \
  --console pty,target_type=serial \
  --noautoconsole \
  --hvm --accelerate \
  --vnc \
  --virt-type=kvm \
  --boot hd --import
