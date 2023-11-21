#!/bin/bash
<<<<<<< HEAD:Lab/dc_with_vEX/config/hosts/run_vm.sh
VM=vm1
=======
VM=dhcp
>>>>>>> a8d6b43 (update):Lab/dc_with_vjunos/config/hosts/run_vm.sh
DISK=${VM}.img
CDROM=./seed_debian.iso
virt-install --name ${VM} \
    --disk ./${DISK},device=disk \
    --disk ${CDROM},device=cdrom \
    --ram 2048 --vcpu 1  \
    --osinfo debian12 \
    --network=bridge:ovs1,model=virtio,virtualport_type=openvswitch \
    --xml './devices/interface/vlan/tag/@id=120' \
    --console pty,target_type=serial \
    --noautoconsole \
    --hvm --accelerate  \
    --vnc  \
    --virt-type=kvm  \
    --boot hd --noreboot


cat << EOF | sudo tee /etc/network/interfaces.d/50-cloud-init
auto lo
iface lo inet loopback

auto enp1s0
iface enp1s0 inet static
address 192.168.201.1/24
gateway 192.168.201.254

iface enp1s0 inet6 static
address fc00:dead:beef:b202::1000:1/64
gateway fc00:dead:beef:b202::1
EOF



#!/bin/bash
VM=vm1
DISK=${VM}.img
CDROM=./seed.iso
virt-install --name ${VM} \
    --disk ./${DISK},device=disk \
    --ram 1024 --vcpu 1  \
    --osinfo alpinelinux3.18 \
    --network=bridge:ovs0,model=virtio,virtualport_type=openvswitch \
    --xml './devices/interface/vlan/tag/@id=201' \
    --console pty,target_type=serial \
    --noautoconsole \
    --hvm --accelerate  \
    --vnc  \
    --virt-type=kvm  \
    --boot hd



#!/bin/bash
VM=vm1
DISK=${VM}.img
CDROM=./seed.iso
virt-install --name ${VM} \
    --disk ./${DISK},device=disk \
    --ram 1024 --vcpu 1  \
    --osinfo alpinelinux3.15 \
    --network=bridge:ovs0,model=virtio,virtualport_type=openvswitch \
    --xml './devices/interface/vlan/tag/@id=201' \
    --console pty,target_type=serial \
    --noautoconsole \
    --hvm --accelerate  \
    --vnc  \
    --virt-type=kvm  \
    --boot hd

    
cat << EOF | tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.201.1/24
gateway 192.168.201.254

iface eth0 inet6 static
address fc00:dead:beef:a201::1000:1/64
gateway fc00:dead:beef:a201::1
EOF

cat << EOF | sudo /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF

hostname vm1 
hostname | tee /etc/hostname



cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.202.2/24
gateway 192.168.202.254

iface eth0 inet6 static
address fc00:dead:beef:a202::1000:2/64
gateway fc00:dead:beef:a202::1
EOF

cat << EOF | sudo /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF

sudo hostname vm2
hostname | sudo tee /etc/hostname



cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.203.3/24
gateway 192.168.203.254

iface eth0 inet6 static
address fc00:dead:beef:a203::1000:3/64
gateway fc00:dead:beef:a203::1
EOF

cat << EOF | sudo /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF

sudo hostname vm3
hostname | sudo tee /etc/hostname

