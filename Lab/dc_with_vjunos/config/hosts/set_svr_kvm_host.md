# node SVR
#!/bin/bash
VM=svr5
MAC=56:04:1a:00:3a:10
IPv4=192.168.12.5/24
IPv6=fc00:dead:beef:a012::1000:5/64
GWv4=192.168.12.254
GWv6=fc00:dead:beef:a012::1
sudo hostname ${VM}
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/netplan/01_net.yaml
network:
  ethernets:
    eth0:
      dhcp4: no
    eth1:
      dhcp4: no
  bonds:
    bond0:
      macaddress: ${MAC}
      interfaces:
        - eth0
        - eth1
      parameters:
         mode: 802.3ad
      addresses: [ ${IPv4} , ${IPv6}]
      routes:
      - to: 0.0.0.0/0
        via: ${GWv4}
      - to: ::/0
        via: ${GWv6}
      nameservers:
        addresses: [8.8.8.8,8.8.4.4]
EOF
uuidgen | sed -e "s/-//g" | sudo tee /etc/machine-id
sudo netplan apply


# node KVM
MAC=56:04:1a:00:3a:be
#!/bin/bash
cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  ethernets:
    eth1:
      dhcp4: no
      mtu: 9000
    eth2:
      dhcp4: no
      mtu: 9000
  bridges:
    ovs0:
      openvswitch: {}
      interfaces:
      - bond0
  bonds:
    bond0:
      macaddress: ${MAC}
      mtu: 9000
      interfaces:
        - eth1
        - eth2
      parameters:
         mode: 802.3ad
EOF
sudo netplan apply


# Download image

lxc image copy images:alpine/edge local: --alias alpine
lxc image copy --vm images:alpine/edge local: --alias alpineVM

# Start LXC instance
lxc launch alpine --name lxc


export LXC_NAME=vm1
export VLAN=11
export OVS=ovs0
export IPv4=192.168.11.102/24
export GWv4=192.168.11.254
export IPv6=192.168.11.102/24
export GWv6=192.168.11.254


echo "Creating VM ${LXC_NAME}"
lxc copy lxc ${LXC_NAME}
lxc query --request PATCH /1.0/instances/${LXC_NAME} --data "{
  \"devices\": {
    \"eth0\" :{
       \"name\": \"eth0\",
       \"nictype\": \"bridged\",
       \"parent\": \"${OVS}\",
       \"vlan\" : \"${VLAN}\",
       \"type\": \"nic\"
    }
  }
}"
echo "push configuration into node ${LXC_NAME}"
cat << EOF | tee ./interface.conf
auto eth0
iface eth0 inet static
    address ${IPv4}
    mtu 1500
    gateway ${GWv4}
iface eth0 inet6 static
    address ${IPv6}
    gateway ${GWv6}
EOF

lxc file push ./interface.conf ${LXC_NAME}/etc/network/interfaces
cat << EOF | tee ./resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
lxc file push ./interface.conf ${LXC_NAME}/etc/resolv.conf


## alpine on KVM
export VM=vm2kvm3
export DISK=${VM}.img
VLAN=12
LAN=ovs0
export IPv4=192.168.12.132/24
export GWv4=192.168.12.254
export IPv6=fc00:dead:beef:a012::1000:132/64
export GWv6=fc00:dead:beef:a012::1
qemu-img create -b alpine.qcow2 -f qcow2 -F qcow2 ${DISK}
virt-install --name ${VM} \
  --disk ./${DISK},device=disk,bus=virtio \
  --ram 512 --vcpu 1 --osinfo alpinelinux3.18 \
  --network=bridge:${LAN},model=virtio,virtualport_type=openvswitch \
  --xml "./devices/interface/vlan/tag/@id=${VLAN}" \
  --xml "./devices/interface/target/@dev=${VM}_e0" \
  --console pty,target_type=serial \
  --noautoconsole \
  --hvm --accelerate \
  --vnc \
  --virt-type=kvm \
  --boot hd --noreboot --import

mkdir ./tmp
sudo modprobe nbd max_part=8
sudo qemu-nbd --connect=/dev/nbd0 ./${DISK}
sudo mount /dev/nbd0p3 ./tmp

cat << EOF | sudo tee tmp/etc/hostname 
${VM}
EOF


cat << EOF | sudo tee tmp/etc/network/interfaces 
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address ${IPv4}
gateway ${GWv4}
iface eth0 inet6 static
address ${IPv6}
gateway ${GWv6}
EOF
cat << EOF | sudo tee tmp/etc/resolv.conf 
nameserver 10.49.32.95
nameserver 10.49.32.97
EOF

sudo umount ./tmp
sudo qemu-nbd --disconnect /dev/nbd0
sleep 1
sudo rmmod nbd


## node HBR

#!/bin/bash
VM=svr4
IPv4ETH0=192.168.201.104/24
IPv6ETH0=fc00:dead:beef:a201::1000:104/64
IPv4ETH1=192.168.202.104/24
IPv6ETH1=fc00:dead:beef:a202::1000:104/64

sudo hostname ${VM}
hostname | sudo tee /etc/hostname
cat << EOF | sudo tee /etc/netplan/01_net.yaml
network:
  ethernets:
    eth0:
      dhcp4: no
      addresses: [ ${IPv4ETH0} , ${IPv6ETH0}]
      nameservers:
        addresses: [8.8.8.8,8.8.4.4]
    eth1:
      dhcp4: no
      addresses: [ ${IPv4ETH1} , ${IPv6ETH1}]
      nameservers:
        addresses: [8.8.8.8,8.8.4.4]
EOF
uuidgen | sed -e "s/-//g" | sudo tee /etc/machine-id
sudo netplan apply

#### CRPD install
## installing cRPD
sudo podman load -i junos-routing-crpd-docker-amd64-24.2R1.14.tgz
export CRPD_NAME=hbr
sudo podman volume create ${CRPD_NAME}-config
sudo podman volume create ${CRPD_NAME}-varlog
sudo podman run --rm --detach --name ${CRPD_NAME} -h ${CRPD_NAME} \
       --net=host --privileged \
       -v ${CRPD_NAME}-config:/config \
       -v ${CRPD_NAME}-varlog:/var/log \
       -it localhost/crpd:24.2R1.14