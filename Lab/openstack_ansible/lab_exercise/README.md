# creating project
for i in demo{1..3}
do
openstack project create ${i}
openstack role add --project ${i} --user admin admin
done

## creating flavor
openstack flavor create --public --vcpus 1 --ram 128 --disk 1 m1.tiny   
openstack flavor create --public --vcpus 1 --ram 2048 --disk 10 m1.small 
openstack flavor create --public --vcpus 2 --ram 4096 --disk 40 m1.medium
openstack flavor create --public --vcpus 2 --ram 8192 --disk 60 m1.large

# uploading image

openstack image create --public --disk-format qcow2 --container-format bare --file cirros-0.6.1-x86_64-disk.img cirros
openstack image create --public --disk-format qcow2 --container-format bare --file debian-11-generic-amd64.qcow2 debian
openstack image create --public --disk-format qcow2 --container-format bare --file jammy-server-cloudimg-amd64.img ubuntu



openstack network create blue 
openstack subnet create --network blue --subnet-range 192.168.101.0/24 --dhcp --gateway 192.168.101.1 --dns-nameserver 8.8.8.8 blue

openstack network create public1 --external --provider-network-type vlan --provider-segment 101 --provider-physical-network vlan
openstack subnet create --network public1 --subnet-range 172.16.101.0/28 --allocation-pool start=172.16.101.2,end=172.16.101.14 --dns-nameserver 8.8.8.8 --dhcp --gateway 172.16.101.1 public1

openstack router create router1
openstack router add subnet router1 blue
openstack router set --external-gateway public1 router1 --fixed-ip subnet=public1,ip-address=172.16.101.2


openstack security group create allow1
openstack security group  rule create --ingress --protocol tcp --dst-port 22 allow1
openstack security group  rule create --ingress --protocol icmp allow1

openstack floating ip create --floating-ip-address 172.16.101.14 public1

openstack server add floating ip vm2 172.16.101.14

openstack server add security group vm2 allow1


openstack keypair create  --public-key ~/.ssh/id_rsa.pub key1

openstack volume create --size 1 --bootable --image cirros vm4
openstack server create --flavor m1.tiny --volume vm4 --network Blue --key key1 vm4
openstack floating ip create --floating-ip-address 172.16.101.5 public1

openstack volume create --bootable --image debian --size 10 vm3

openstack server create --flavor m1.small --volume vm3 --network blue --key key1 --security-group allow1 vm3
openstack floating ip create --floating-ip-address 172.16.101.13 public1

openstack server add floating ip vm3 172.16.101.13


openstack server remove floating ip vm5 172.16.101.10

# enable distributed routing (DVR)
on neutron container, edit file /etc/neutron/neutron, and add the following

cat << EOF | sudo tee -a /etc/neutron/neutron.conf
[ovn]
enable_distributed_floating_ip = True
EOF

openstack network create red
openstack subnet create --network red --subnet-range 192.168.102.0/24 --dhcp --gateway 192.168.102.1 --dns-nameserver 8.8.8.8 red

openstack volume create --size 10 --bootable --image ubuntu gw1
openstack server create --flavor m1.small --volume gw1 --nic net-id=fd925e4c-6605-48ac-9b0a-c4d2e8a1918b --nic net-id=c3cfb45c-c36c-438e-936c-715f174f6ac1,v4-fixed-ip=192.168.102.1  --security-group allow1 --key key1 gw1

openstack server create --flavor m1.small --volume gw1 --network public1 --network red  --security-group allow1 --key key1 gw1
