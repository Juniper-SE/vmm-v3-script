# using openstack
 1. create image

        openstack image create --public --disk-format qcow2 --container-format bare --file cirros-0.6.3-x86_64-disk.img cirros
        openstack image create --public --disk-format qcow2 --container-format bare --file debian-12-generic-amd64.qcow2 debian
        openstack image create --public --disk-format qcow2 --container-format bare --file noble-server-cloudimg-amd64.img ubuntu24.04


 2. create flavor

        openstack flavor create --public --ram 2048 --disk 10 --vcpus 1 m1.small1
        openstack flavor create --public --ram 512 --disk 10 --vcpus 1 m1.small0
        openstack flavor create --public --ram 4096 --disk 40 --vcpus 2 m1.medium
        openstack flavor create --public --ram 256 --disk 1 --vcpus 1 m1.tiny

 3. create external network

        openstack network create --external --share --provider-network-type vlan --provider-segment 111 --provider-physical-network physnet1 ext_net111
        openstack subnet create --network ext_net111 --no-dhcp --gateway 192.168.111.1 --subnet-range 192.168.111.0/24 --allocation-pool start=192.168.111.10,end=192.168.111.200 ext_subnet111
        openstack subnet create --network ext_net111 --no-dhcp --gateway  fc00:dead:beef:a111::1 --subnet-range  fc00:dead:beef:a111::/64 --allocation-pool start=fc00:dead:beef:a111::ffff:1,end=fc00:dead:beef:a111::ffff:ffff --ip-version 6 ext_subnet111_v6

 4. create other user

        openstack domain create domain1
        openstack project create --domain domain1 project1
        openstack role add --user admin --project project1 member
        openstack role add --user admin --project project1 Admin
        openstack user create --domain domain1 --project project1 --password-prompt user1


 5. create network for project

        export OS_PROJECT_DOMAIN_NAME=domain1
        export OS_PROJECT_NAME=project1

        openstack network create --internal project1_net
        openstack subnet create --network project1_net --dns-nameserver 10.49.32.95 --subnet-range 172.16.111.0/24 --allocation-pool start=172.16.111.11,end=172.16.111.200 project1_subnet
        openstack subnet create --network project1_net --ip-version 6 --dns-nameserver 2001:4860:4860::8888 --subnet-range fc00:dead:beef:b111::/64 --allocation-pool start=fc00:dead:beef:b111::ffff:1,end=fc00:dead:beef:b111::ffff:ffff --gateway fc00:dead:beef:b111::1 --ipv6-ra-mode dhcpv6-stateful --ipv6-address-mode dhcpv6-stateful project1_subnet_v6

        openstack router create project1_router
        openstack router add subnet project1_router project1_subnet
        openstack router add subnet project1_router project1_subnet_v6
        openstack router set project1_router --external-gateway ext_net111

        openstack security group create --description "This is the new SG" SG1
        openstack security group rule create --ingress --protocol icmp --remote-ip 0.0.0.0/0 SG1
        openstack security group rule create --ingress --protocol icmp --remote-ip ::/0 --ethertype ipv6 SG1
        openstack security group rule create --ingress --protocol tcp --dst-port 22  --remote-ip ::/0 --ethertype ipv6 SG1
        openstack security group rule create --ingress --protocol tcp --dst-port 22  --remote-ip 0.0.0.0/0  SG1

6. Create VMs for the project


        openstack port create --network project1_net --fixed-ip subnet=project1_subnet,ip-address=172.16.111.101 --fixed-ip subnet=project1_subnet_v6,ip-address=fc00:dead:Beef:b111::ffff:101 --security-group SG1 port_vm1
        openstack server create --image debian --flavor m1.small1 --key-name key1 --boot-from-volume 10 --port port_vm1 vm1
       
        openstack port create --network project1_net --fixed-ip subnet=project1_subnet,ip-address=172.16.111.102 --fixed-ip subnet=project1_subnet_v6,ip-address=fc00:dead:Beef:b111::ffff:102 --security-group SG1 port_vm2
        openstack server create --image cirros --flavor m1.tiny --key-name key1 --boot-from-volume 1 --port port_vm2 vm2

        openstack volume create --size 10 --image debian --bootable disk3_vm5
        openstack port create --network project1_net --fixed-ip subnet=project1_subnet,ip-address=172.16.111.105 --fixed-ip subnet=project1_subnet_v6,ip-address=fc00:dead:Beef:b111::ffff:105 --security-group SG1 port_vm5
        openstack server create --flavor m1.small1 --key-name key1 --port port_vm5 --volume disk3_vm5 vm5
        openstack floating ip  create --floating-ip-address 192.168.111.115 --port port_vm5 ext_net111