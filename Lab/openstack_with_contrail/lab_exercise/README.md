# This provide guideline on how to the lab

172.16.12.10 node0
172.16.12.11 node1
172.16.12.12 node2
172.16.12.13 node3
172.16.12.14 node4

sudo -s 
cd /etc/kolla/kolla-toolbox
curl -L -O https://download.cirros-cloud.net/0.5.2/cirros-0.5.2-x86_64-disk.img
curl -L -O https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
curl -L -O https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-generic-amd64.qcow2

sudo mv cirros-0.5.2-x86_64-disk.img /etc/kolla/kolla-toolbox
sudo mv focal-server-cloudimg-amd64.img /etc/kolla/kolla-toolbox
sudo mv debian-11-generic-amd64.qcow2 /etc/kolla/kolla-toolbox

docker exec -it kolla_toolbox sh 
cd /var/lib/kolla/config_files
source ./admin-openrc.sh

openstack project create demo1
openstack project create demo2
openstack role add --project demo1 --user admin admin
openstack role add --project demo2 --user admin admin

## creating flavor
openstack flavor create --public --vcpus 1 --ram 128 --disk 1 m1.tiny   
openstack flavor create --public --vcpus 1 --ram 2048 --disk 10 m1.small 
openstack flavor create --public --vcpus 2 --ram 4096 --disk 40 m1.medium
openstack flavor create --public --vcpus 2 --ram 8192 --disk 60 m1.large

# uploading image

openstack image create --public --disk-format qcow2 --container-format bare --file cirros-0.5.2-x86_64-disk.img cirros
openstack image create --public --disk-format qcow2 --container-format bare --file debian-11-generic-amd64.qcow2 debian11
openstack image create --public --disk-format qcow2 --container-format bare --file focal-server-cloudimg-amd64.img ubuntu20.04


