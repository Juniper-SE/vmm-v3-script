sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst openvswitch-switch

virsh net-destroy default
virsh net-undefine default



create ovs-switch
sudo ovs-vsctl add ovs1
sudo ovs-vsctl add-port ovs1 bond0


#!/bin/bash
VM=vm1g1
DISK=${VM}.img
LAN=ovs1
virt-install --name ${VM} \
  --disk ./${DISK},device=disk,bus=virtio \
  --ram 256 --vcpu 1 --osinfo alpinelinux3.15 \
  --network=bridge:${LAN},model=virtio,virtualport_type=openvswitch \
  --xml './devices/interface/vlan/tag/@id=101' \
  --console pty,target_type=serial \
  --noautoconsole \
  --hvm --accelerate \
  --vnc \
  --virt-type=kvm \
  --boot hd



#!/bin/bash
VM=vm1
DISK=${VM}.img
LAN=ovs1
virt-install --name ${VM} \
  --disk ./${DISK},device=disk,bus=virtio \
  --disk ./seed.iso,device=cdrom \
  --ram 2048 --vcpu 1 --osinfo debian12 \
  --network=bridge:${LAN},model=virtio,virtualport_type=openvswitch \
  --xml './devices/interface/vlan/tag/@id=160' \
  --xml "./devices/interface/target/@dev=${VM}"
  --console pty,target_type=serial \
  --noautoconsole \
  --hvm --accelerate \
  --vnc \
  --virt-type=kvm \
  --boot hd





on hypervisor LXC1

sudo hostname vm1
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
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

cat << EOF | sudo tee /etc/resolv.conf
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
address 192.168.202.1/24
gateway 192.168.202.254
iface eth0 inet6 static
address fc00:dead:beef:a202::1000:1/64
gateway fc00:dead:beef:a202::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF


sudo hostname vm3
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.201.3/24
gateway 192.168.201.254
iface eth0 inet6 static
address fc00:dead:beef:a201::1000:3/64
gateway fc00:dead:beef:a201::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF


sudo hostname vm4g1
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback


set system services ssh protocol-version v2
set system authentication-order password
set system login user mist class super-user
set system login user mist authentication encrypted-password $6$a6CnQuPwt3INdBcr$fmUWMK4RBHpHI.HM8hd6JwYmdiV00HE417tow0UJtCf1eA1/UixRIt6gMbTWzPQa9Ek029o23lTZfZCqANupl.
set system login user mist authentication ssh-rsa "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7CBV65hh09uH+Hh7bDeJ2/NQ5aId84qScCXucl6pmSVVJEtpkEMQGLKvFpcz3NZ0JaG9Fgp/IqWcJ+iQJIstsbQ2+6yPxfghvZRqYByzeqCYuCASt693SiPmQyYF1KjQuWXiLqH4AoiITvWiS+OF5old7qeH17dsDTWaH/0ZfV8nv+PMEsBsc6AFV6tRZ+7wxPyysD5hyVEcpPf4i1ihIOuYVEtVHGidnEgSE+f1L2A11m/lveMIARdkyr2a4XXoIH/mZjAX4372eRGiPCPn6QkfphtP2PY5WoGVZo0PH1xQBLbaW8xfSk8ET02LA5MAL6i5D8n4pVkVmwcOpPfysEiCpbX+YrsgP8hP8CB9iMN3F/ONk2umsGOMwT0VhX2zgXg99LMR3+uotkG61TcPTDTLnJSo75FSmozGejan4iaU5gF3rGyn9hiZKC4ollwjqs0wCygjL+ir2EA8XqQne65UKxmDR8y7SK/8Bc+hUjKbasu9vcKm5uI1UiAbvbSE= mist@1cdb9bf7-3ed9-4b51-95e4-fd5d542b10e9"
set system services outbound-ssh client mist device-id 1cdb9bf7-3ed9-4b51-95e4-fd5d542b10e9
set system services outbound-ssh client mist secret 2e85704fef4bfaadbfc00f28dd1a77bc71fe3f79b67d46fc419b3f17b5bc0803829953d953e2d101a26329aa736a195300a8727ddbcb2a4473a8384fa1f92b8e
set system services outbound-ssh client mist services netconf keep-alive retry 12 timeout 5
set system services outbound-ssh client mist oc-term.mistsys.net port 2200 timeout 60 retry 1000
delete system phone-home

auto eth0
iface eth0 inet static
address 192.168.3.4/24
gateway 192.168.3.254
iface eth0 inet6 static
address 2001:dead:beef:aa03::1000:4/64
gateway 2001:dead:beef:aa03::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF


sudo hostname vm5g1
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.3.5/24
gateway 192.168.3.254
iface eth0 inet6 static
address 2001:dead:beef:aa03::1000:5/64
gateway 2001:dead:beef:aa03::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF



sudo hostname vm6g1
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.4.6/24
gateway 192.168.4.254
iface eth0 inet6 static
address 2001:dead:beef:aa04::1000:6/64
gateway 2001:dead:beef:aa04::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF



sudo hostname vm7g1
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.4.7/24
gateway 192.168.4.254
iface eth0 inet6 static
address 2001:dead:beef:aa04::1000:7/64
gateway 2001:dead:beef:aa04::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF


sudo hostname vm8g1
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.4.8/24
gateway 192.168.4.254
iface eth0 inet6 static
address 2001:dead:beef:aa04::1000:8/64
gateway 2001:dead:beef:aa04::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF

sudo hostname vm1g2
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.31.1/24
gateway 172.16.31.254
iface eth0 inet6 static
address 2001:dead:beef:ff31::1000:1/64
gateway 2001:dead:beef:ff31::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF


sudo hostname vm2g2
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.31.2/24
gateway 172.16.31.254
iface eth0 inet6 static
address 2001:dead:beef:ff31::1000:2/64
gateway 2001:dead:beef:ff31::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF


sudo hostname vm3g2
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.31.3/24
gateway 172.16.31.254
iface eth0 inet6 static
address 2001:dead:beef:ff31::1000:3/64
gateway 2001:dead:beef:ff31::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF


sudo hostname vm4g2
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.31.4/24
gateway 172.16.31.254
iface eth0 inet6 static
address 2001:dead:beef:ff31::1000:4/64
gateway 2001:dead:beef:ff31::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF

sudo hostname vm1vnet33
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.33.1/24
gateway 172.16.33.254
iface eth0 inet6 static
address 2001:dead:beef:ff33::1000:1/64
gateway 2001:dead:beef:ff33::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF


sudo hostname vm1vnet34
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.34.1/24
gateway 172.16.34.254
iface eth0 inet6 static
address 2001:dead:beef:ff34::1000:1/64
gateway 2001:dead:beef:ff34::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF







sudo hostname vm1
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.201.1/24
gateway 192.168.201.254
iface eth0 inet6 static
address 2001:dead:beef:201::1000:1/64
gateway 2001:dead:beef:201::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF


sudo hostname vm2
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.201.2/24
gateway 192.168.201.254
iface eth0 inet6 static
address 2001:dead:beef:201::1000:2/64
gateway 2001:dead:beef:201::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF


sudo hostname vm3
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.203.3/24
gateway 192.168.203.254
iface eth0 inet6 static
address 2001:dead:beef:203::1000:3/64
gateway 2001:dead:beef:203::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF



on hypervisor SVR5


sudo hostname vm1
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.201.1/24
gateway 172.16.201.254
iface eth0 inet6 static
address 2001:dead:ffff:201::1000:1/64
gateway 2001:dead:ffff:201::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF

sudo hostname vm3
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.203.3/24
gateway 172.16.203.254
iface eth0 inet6 static
address 2001:dead:ffff:203::1000:3/64
gateway 2001:dead:ffff:203::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF


on LXC2

sudo hostname vm1
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.31.1/24
gateway 172.16.31.254
iface eth0 inet6 static
address 2001:dead:ffff:31::1000:1/64
gateway 2001:dead:ffff:31::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF

sudo hostname vm2
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 172.16.32.2/24
gateway 172.16.32.254
iface eth0 inet6 static
address 2001:dead:ffff:32::1000:2/64
gateway 2001:dead:ffff:32::1
EOF

cat << EOF | sudo tee /etc/resolv.conf
nameserver 66.129.233.81
nameserver 66.129.233.82
EOF

