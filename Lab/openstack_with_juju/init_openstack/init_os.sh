#!/bin/bash
echo "download and create disk image"
curl -L -O https://download.cirros-cloud.net/0.5.2/cirros-0.5.2-x86_64-disk.img
curl -L -O https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
curl -L -O https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-generic-amd64.qcow2
openstack image create --file cirros-0.5.2-x86_64-disk.img --disk-format qcow2 --container-format bare --public cirros
openstack image create --file focal-server-cloudimg-amd64.img --disk-format qcow2 --container-format bare --public ubuntu
openstack image create --file debian-11-generic-amd64.qcow2 --disk-format qcow2 --container-format bare --public debian

echo "Create flavor"
openstack flavor create --public --vcpu 1 --disk 1 --ram 128 --public m1.tiny
openstack flavor create --public --vcpu 1 --disk 10 --ram 2048 --public m1.small
openstack flavor create --public --vcpu 2 --disk 40 --ram 4096 --public m1.medium
openstack flavor create --public --vcpu 2 --disk 80 --ram 8192 --public m1.large
echo "Create project"
openstack project create --domain admin_domain demo1
openstack project create --domain admin_domain demo2
openstack role add --user admin --project demo1 admin
openstack role add --user admin --project demo2 admin
