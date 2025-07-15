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
        - 10.100.1.0/31
        #- fc00:dead:beef:1001::0/127
    eth2:
      dhcp4: false
      mtu: 9000
      addresses: 
        - 10.100.1.2/31
        # - fc00:dead:beef:1001::2/127
  vlans:
    eth3.101:
      dhcp4: false
      id: 101
      link: eth3
      addresses:
        - 192.168.11.1/24
        - fc00:dead:beef:a011::1/64 
EOF

cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  vlans:
    eth3.101:
      dhcp4: false
      id: 101
      link: eth3
      addresses:
        - 192.168.11.1/24
        - fc00:dead:beef:a011::1/64 
EOF

sudo netplan apply

cat << EOF | sudo tee /etc/dhcp/dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
subnet 192.168.11.0 netmask 255.255.255.0 {
 range 192.168.11.11 192.168.11.100;
 option routers 192.168.11.1;
}
EOF
sudo systemctl restart isc-dhcp-server 


### installing CRPD

podman load -i junos-routing-crpd-docker-amd64-24.2R1.14.tgz
podman volume create crpd12-config
podman volume create crpd12-varlog

podman run --rm --detach --name crpd12 -h crpd12 --net=host --privileged -v crpd12-config:/config -v crpd12-varlog:/var/log -it localhost/crpd:24.2R1.14


sudo sed -i -e "s/isisd=no/isisd=yes/" /etc/frr/daemons 
sudo sed -i -e "s/bgpd=no/bgpd=yes/" /etc/frr/daemons 

cat << EOF | sudo tee -a /etc/frr/frr.conf
!
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
 net 49.0001.0001.0001.0011.00
exit
!
end
EOF

sudo systemctl restart frr
