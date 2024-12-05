cat << EOF | sudo tee /etc/netplan/02_net.yaml
network:
  ethernets:       
    eth1:
      dhcp4: false
      mtu: 9000
      addresses:
        - 10.100.1.1/31
        #- fc00:dead:beef:1001::1/127
       
    eth2:
      dhcp4: false
      mtu: 9000
      addresses:
        - 10.100.1.5/31
        #- fc00:dead:beef:1001::5/127
EOF

sudo netplan apply

sudo sed -i -e "s/isisd=no/isisd=yes/" /etc/frr/daemons 

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
router isis test1
 is-type level-2-only
 net 49.0001.0001.0001.0001.00
exit
!
end
EOF

sudo systemctl restart frr
