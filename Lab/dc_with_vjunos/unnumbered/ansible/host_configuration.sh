
sudo hostname svr1
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
      macaddress: 56:04:20:00:91:18
      interfaces:
        - eth0
        - eth1
      parameters:
         mode: 802.3ad
      addresses: [ 192.168.10.1/24, fc00:dead:beef:10::1000:1/64]
      gateway4: 192.168.10.254
      gateway6:  fc00:dead:beef:10::1
      nameservers:
        addresses: [8.8.8.8,8.8.4.4]
EOF

forwarding-options {
    evpn-vxlan {
        shared-tunnels;
    }
}


sudo hostname svr3
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
      macaddress: 56:04:20:00:91:21
      interfaces:
        - eth0
        - eth1
      parameters:
         mode: 802.3ad
      addresses: [ 192.168.10.3/24, fc00:dead:beef:10::1000:3/64]
      gateway4: 192.168.10.254
      gateway6:  fc00:dead:beef:10::1
      nameservers:
        addresses: [8.8.8.8,8.8.4.4]
EOF


sudo hostname svr2
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
      macaddress: 56:04:20:00:91:2a
      interfaces:
        - eth0
        - eth1
      parameters:
         mode: 802.3ad
      addresses: [ 192.168.20.2/24, fc00:dead:beef:20::1000:2/64]
      gateway4: 192.168.20.254
      gateway6:  fc00:dead:beef:20::1
      nameservers:
        addresses: [8.8.8.8,8.8.4.4]
EOF

