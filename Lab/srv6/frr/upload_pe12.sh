cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  ethernets:       
    eth3:
      dhcp4: false
      mtu: 9000
       
    eth1:
      dhcp4: false
      mtu: 9000
      addresses:
        - 10.100.1.4/31
        #- fc00:dead:beef:1001::4/127
       
    eth2:
      dhcp4: false
      mtu: 9000
      addresses:
        - 10.100.1.6/31
        #- fc00:dead:beef:1001::6/127
  vlans:
    eth3.101:
      dhcp4: false
      id: 101
      link: eth3
      addresses:
        - 192.168.12.1/24
        - fc00:dead:beef:a012::1/64
EOF

sudo netplan apply


cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  vlans:
    eth3.101:
      dhcp4: false
      id: 101
      link: eth3
      addresses:
        - 192.168.12.1/24
        - fc00:dead:beef:a012::1/64
EOF

sudo netplan apply

cat << EOF | sudo tee /etc/dhcp/dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
subnet 192.168.12.0 netmask 255.255.255.0 {
 range 192.168.12.11 192.168.12.100;
 option routers 192.168.12.1;
}
EOF
sudo systemctl restart isc-dhcp-server 


###
installing CRPD
sysctl -w net.ipv4.fib_multipath_hash_policy=1
sysctl -w net.ipv6.fib_multipath_hash_policy=1


### 
installing FRR


sudo sed -i -e "s/isisd=no/isisd=yes/" /etc/frr/daemons 
sudo sed -i -e "s/bgpd=no/bgpd=yes/" /etc/frr/daemons 

cat << EOF | sudo tee -a /etc/frr/frr.conf
interface eth1
 ip router isis test1
 ipv6 router isis test1
 isis circuit-type level-2-only
 isis network point-to-point
exit
!
interface eth2
 ip router isis test1
 ipv6 router isis test1
 isis circuit-type level-2-only
 isis network point-to-point
exit
!
interface eth3.101
 ip router isis test1
 ipv6 router isis test1
exit
!
router isis test1
 is-type level-2-only
 net 49.0001.0001.0001.0012.00
exit
!
end
EOF

sudo systemctl restart frr
