# using openstack
 1. create image

        openstack image create --public --disk-format qcow2 --container-format bare --file /home/irzan/Downloads/cirros-0.6.3-x86_64-disk.img cirros
        openstack image create --public --disk-format qcow2 --container-format bare --file /home/irzan/Downloads/debian-12-generic-amd64.qcow2 debian
        openstack image create --public --disk-format qcow2 --container-format bare --file /home/irzan/Downloads/jammy-server-cloudimg-amd64.img ubuntu22.04
        openstack image create --public --disk-format qcow2 --container-format bare --file /home/irzan/Downloads/noble-server-cloudimg-amd64.img ubuntu24.04


 2. create flavor

        openstack flavor create --public --ram 2048 --disk 10 --vcpus 1 m1.small1
        openstack flavor create --public --ram 512 --disk 10 --vcpus 1 m1.small0
        openstack flavor create --public --ram 4096 --disk 40 --vcpus 2 m1.medium
        openstack flavor create --public --ram 256 --disk 1 --vcpus 1 m1.tiny

 3. create external network

        openstack network create --external --share --provider-network-type vlan --provider-segment 112 --provider-physical-network physnet1 ext_net112
        openstack subnet create --network ext_net112 --no-dhcp --gateway 192.168.112.254 --subnet-range 192.168.112.0/24 --allocation-pool start=192.168.112.1,end=192.168.112.200 ext_subnet112
        openstack subnet create --network ext_net112 --no-dhcp --gateway  fc00:dead:beef:a112::ffff --subnet-range  fc00:dead:beef:a112::/64 --allocation-pool start=fc00:dead:beef:a112::ffff:1,end=fc00:dead:beef:a112::ffff:ffff --ip-version 6 ext_subnet112_v6 

 4. create other user

        openstack domain create domain1
        openstack project create --domain domain1 project1
        openstack role add --user admin --project project1 member
        openstack role add --user admin --project project1 Admin

        openstack user create --domain domain1 --project project1 --password-prompt user1


 5. create network for project

        openstack network create --internal project1_net

        openstack subnet create --network project1_net --dns-nameserver 192.168.10.1 --subnet-range 172.16.111.0/24 --allocation-pool start=172.16.111.11,end=172.16.111.200 project1_subnet

        openstack subnet create --network project1_net --ip-version 6 --dns-nameserver 2001:4860:4860::8888 --subnet-range fc00:dead:beef:b111::/64 --allocation-pool start=fc00:dead:beef:b111::ffff:1,end=fc00:dead:beef:b111::ffff:ffff --gateway fc00:dead:beef:b111::1 --ipv6-ra-mode dhcpv6-stateful --ipv6-address-mode dhcpv6-stateful project1_subnet_v6

        openstack router create project1_router
        openstack router add subnet project1_router project1_subnet
        openstack router add subnet project1_router project1_subnet_v6
        openstack router set project1_router --external-gateway ext_net112

        openstack keypair create --public-key ~/.ssh/id_rsa.pub key1
        openstack security group create --description 'Allow SSH' Allow_SSH
        openstack security group rule create --proto tcp --dst-port 22 Allow_SSH


        openstack security group create --description "This is the new SG" SG1
        openstack security group rule create --ingress --protocol icmp --remote-ip 0.0.0.0/0 SG1
        openstack security group rule create --ingress --protocol icmp --remote-ip ::/0 --ethertype ipv6 SG1
        openstack security group rule create --ingress --protocol tcp --dst-port 22  --remote-ip ::/0 --ethertype ipv6 SG1
        openstack security group rule create --ingress --protocol tcp --dst-port 22  --remote-ip 0.0.0.0/0  SG1

        openstack server create --image cirros --flavor m1.tiny --key-name key1 --network project1_net --boot-from-volume 1  vm1

        openstack server create --image cirros --flavor m1.tiny --key-name key1 --network user1_net --boot-from-volume 1 --security-group Allow_SSH vm1
        openstack server create --image cirros --flavor m1.tiny --key-name key1 --network user1_net --boot-from-volume 1 --security-group Allow_SSH vm2
        openstack server create --image ubuntu22.04 --flavor m1.small1 --key-name key1 --network user1_net --boot-from-volume 10 --security-group Allow_SSH vm3
        openstack server create --image alpine --flavor m1.small1 --key-name key1 --network user1_net --boot-from-volume 10 --security-group Allow_SSH vm4

        openstack port create --network user1_net --fixed-ip subnet=user1_subnet,ip-address=172.16.111.5 --fixed-ip subnet=user1_subnet_v6,ip-address=fc00:dead:Beef:b111::ffff:5 port1

        openstack server create --image cirros --flavor m1.tiny --key-name key1 --boot-from-volume 1 --security-group Allow_SSH --port port1 vm4

        openstack port create --network user1_net --fixed-ip subnet=user1_subnet,ip-address=172.16.111.6 --fixed-ip subnet=user1_subnet_v6,ip-address=fc00:dead:Beef:b111::ffff:6 port2

        openstack server create --image ubuntu22.04 --flavor m1.small1 --key-name key1 --boot-from-volume 10 --security-group Allow_SSH --port port2 vm6

        openstack port create --network user1_net --fixed-ip subnet=user1_subnet,ip-address=172.16.111.7 --fixed-ip subnet=user1_subnet_v6,ip-address=fc00:dead:Beef:b111::ffff:7 port7

        openstack server create --image debian --flavor m1.small1 --key-name key1 --boot-from-volume 10  --port port7 vm7

       openstack security group create --description 'Allow SSH' Allow1
        openstack security group rule create --proto tcp --dst-port 22 Allow1
        

        openstack port create --network user1_net --fixed-ip subnet=user1_subnet,ip-address=172.16.111.6 --fixed-ip subnet=user1_subnet_v6,ip-address=fc00:dead:Beef:b111::ffff:6 port_vm6

        openstack server create --image debian --flavor m1.small0 --key-name user1 --boot-from-volume 10 --security-group Allow_SSH --port port_vm6 vm6

        openstack server create --image debian --flavor m1.small0 --key-name user1 --boot-from-volume 10 --security-group Allow_SSH --network user1_net vm6

        openstack server create --image ubuntu --flavor m1.small --key-name user1 --boot-from-volume 10 --security-group Allow_SSH --network user1_net vm7


        openstack server create --image cirros --flavor m1.tiny --key-name key1 --boot-from-volume 1 --port port6 vm6

        openstack server create --image ubuntu22.04 --flavor m1.small1 --key-name key1 --boot-from-volume 10 --port port6 vm6


        openstack port create --network project1_net --fixed-ip subnet=project1_subnet,ip-address=172.16.111.7 --fixed-ip subnet=project1_subnet_v6,ip-address=fc00:dead:Beef:b111::ffff:7 --security-group SG1 port7
         
        openstack server create --image ubuntu22.04 --flavor m1.small1 --key-name key1 --boot-from-volume 10 --port port7 vm7

        openstack security group create --description 'Allow SSH' SG1
        openstack security group rule create --ingress --proto tcp --dst-port 22 --remote-ip ::/0 --ethertype ipv6 SG10
        openstack security group rule create --ingress --proto tcp --dst-port 22 --remote-ip 0.0.0.0/0  SG10
        openstack security group rule create --ingress --proto icmp --remote-ip ::/0 --ethertype ipv6 SG10
        openstack security group rule create --ingress --proto icmp --remote-ip 0.0.0.0/0  SG10
