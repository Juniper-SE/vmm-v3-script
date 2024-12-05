cat << EOF | sudo vtysh 
enable
config t
router bgp 65200
 neighbor 172.16.11.110 remote-as 65201
 neighbor 172.16.11.111 remote-as 65201
 neighbor 172.16.11.112 remote-as 65201
 neighbor 172.16.16.1  remote-as 64512
 neighbor 172.16.16.3  remote-as 64512
 neighbor 172.16.16.5  remote-as 64512
 neighbor 2001:1010:dead:beef::1:1 remote-as 64512
 neighbor 2001:1010:dead:beef::1:3 remote-as 64512
 neighbor 2001:1010:dead:beef::1:5 remote-as 64512
!
 address-family ipv4 unicast
  network 0.0.0.0/0
 exit-address-family
 address-family ipv6 unicast
  network ::/0
  neighbor 2001:1010:dead:beef::1:1 activate
  neighbor 2001:1010:dead:beef::1:3 activate
  neighbor 2001:1010:dead:beef::1:5 activate
 exit-address-family
!
exit
exit
write mem
exit

EOF
