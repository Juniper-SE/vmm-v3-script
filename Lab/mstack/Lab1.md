# create project and assign user to it

openstack project create --domain users demo1
openstack user create --domain users --password pass01 demo1
openstack role add  --user demo1 --user-domain users --project demo1 admin


openstack network create --external --provider-network-type vlan --provider-segment 102  --share --provider-physical-network physnet1 ext3
openstack subnet create --gateway 172.16.103.1  --subnet-range 172.16.103.0/24 --allocation-pool start=172.16.103.11,end=172.16.103.200 --network ext3  ext3_subnetv4
openstack subnet create --gateway fc00:dead:beef:a103::1  --subnet-range fc00:dead:beef:a103::/64 --ipv6-ra-mode slaac --ipv6-address-mode slaac --ip-version 6 --network ext3 ext3_subnetv6

openstack network create demo3
openstack subnet create --gateway 192.168.103.1  --subnet-range 192.168.103.0/24 --network demo3 demo3_subnetv4
openstack subnet create --gateway fc00:dead:beef:b103::1  --subnet-range fc00:dead:beef:b103::/64 --ipv6-ra-mode slaac --ipv6-address-mode slaac  --ip-version 6 --network demo3 demo3_subnetv6

openstack router create --enable-snat --external-gateway ext3 demo3-router
openstack router add subnet demo3-router demo3_subnetv4
openstack router add subnet demo3-router demo3_subnetv6

openstack security group create SG1
openstack security group rule create --ingress --protocol icmp --remote-ip 0.0.0.0/0 SG1
openstack security group rule create --ingress --protocol ipv6-icmp --remote-ip ::/0 SG1
openstack security group rule create --ingress --protocol tcp --dst-port 22 --remote-ip 0.0.0.0/0 SG1
openstack security group rule create --ingress --ethertype IPV6 --protocol tcp --dst-port 22 --remote-ip ::/0 SG1

openstack keypair create --public-key ./key1.pub key1

openstack volume create --size 10 --image ubuntu --bootable ubuntu1
openstack volume create --size 2 --image cirros --bootable cirros1
openstack server create --network demo3 --key-name key1 --security-group SG1 --volume ubuntu2 --flavor m1.small ubuntu2
openstack server create --network demo3 --key-name key1 --security-group SG1 --volume 93dd01d3-a1e8-4b44-aa55-7a3197ffc7b4 --flavor m1.tiny cirros1