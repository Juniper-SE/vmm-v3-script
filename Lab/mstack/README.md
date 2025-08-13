# hosts
    cat << EOF | sudo tee -a /etc/hosts
    172.16.11.111 node1
    172.16.11.112 node2
    172.16.11.113 node3
    172.16.11.114 node4
    EOF


# first node
    sudo snap install openstack
    sunbeam prepare-node-script --bootstrap | bash -x && newgrp snap_daemon
    sunbeam cluster bootstrap --role control,compute,storage
    # sunbeam configure --openrc demo-openrc
    sunbeam configure
    for i in node{2..5}
    do
        sunbeam cluster add ${i}. --output ${i}.asc
        scp ${i}.asc ${i}:~/
    done
    sunbeam cluster resize
    sunbeam cluster list


# next node
    sudo snap install openstack
    sunbeam prepare-node-script | bash -x && newgrp snap_daemon
    cat nodeX.asc | sunbeam cluster join --role control,compute,storage -
    cat nodeX.asc | sunbeam cluster join --role compute,storage -




# create admin rc file

    sunbeam openrc > admin-openrc

# get openstack dashboard URL

    sunbeam dashboard-url

# download cloud image

    https://download.cirros-cloud.net/
    https://cloud-images.ubuntu.com/

# upload image into openstack
    openstack image create --public --disk-format qcow2 --container-format bare --file cirros-0.6.3-x86_64-disk.img cirros
    openstack image create --public --disk-format qcow2 --container-format bare --file noble-server-cloudimg-amd64.img ubuntu

# create project and user

    openstack project create demo1
    openstack project create demo2
    openstack role add --project demo1 --user admin admin
    openstack role add --project demo2 --user admin admin
    openstack role add --project demo --user admin admin
    openstack role add --domain users --user demo2 --user-domain users admin


    openstack user create --domain <domain> --password <password> <user>
    openstack project create --domain <domain> <project_name>


# create project and user

    openstack project create --domain users demo2
    openstack user create --domain users --password pass01 demo2
    # openstack role add --domain users --user demo2 --user-domain users admin
    openstack role add  --user demo2 --user-domain users --project demo2 admin

# creating flavor
    openstack flavor create --public --vcpus 1 --ram 128 --disk 1 m1.tiny   
    openstack flavor create --public --vcpus 1 --ram 2048 --disk 10 m1.small 
    openstack flavor create --public --vcpus 2 --ram 4096 --disk 40 m1.medium
    openstack flavor create --public --vcpus 2 --ram 8192 --disk 60 m1.large


# create external network

    openstack network create --external --provider-network-type vlan --provider-segment 101  --share --provider-physical-network physnet1 ext1
    openstack subnet create --gateway 172.16.101.1  --subnet-range 172.16.101.0/24 --network ext1 ext1_subnetv4

    openstack network create --external --provider-network-type vlan --provider-segment 102  --share --provider-physical-network physnet1 ext2
    openstack subnet create --gateway 172.16.102.1  --subnet-range 172.16.102.0/24 --allocation-pool start=172.16.102.11,end=172.16.102.200 --network ext2  ext2_subnetv4
    openstack subnet create --gateway fc00:dead:beef:a102::1  --subnet-range fc00:dead:beef:a102::/64 --ipv6-ra-mode slaac --ipv6-address-mode slaac --ip-version 6 --network ext2 ext2_subnetv6

    openstack network create demo2
    openstack subnet create --gateway 192.168.102.1  --subnet-range 192.168.102.0/24 --network demo2 demo2_subnet4
    openstack subnet create --gateway fc00:dead:beef:b102::1  --subnet-range fc00:dead:beef:b102::/64 --ipv6-ra-mode slaac --ipv6-address-mode slaac --ip-version 6 --network demo2 demo2_subnetv6


# add keypair 
    openstack keypair create --public-key <ssh-pub-key-file> <key-name>

# Create volume from image

    openstack volume create --size <size> --bootable --image <image-name> <volume-name>

# create vm instance

    openstack server create --flavor <flavor-name> --volume <volume-name> --key-name <key-name> --network <network-name> <instance-name>

# get instance's console

    openstack console url show --spice cirros1
# create floating ip 

    openstack floating ip create  external-network
    openstack floating ip list

    openstack port list
    openstack floating ip set --port <port-id> <floating-ip>

#  create instance

    openstack volume create --size <size> --bootable --image <image-name> <volume-name>
    openstack floating ip create  <network-name>
    openstack port create --network <network-name> 
    openstack floating ip set --port <port-id> <floating-ip>
    openstack server create --flavor <flavor> --volume <volume-name> --key-name key1 --nic port-id=<port-id> <instance-name>

    openstack port create port 
    

# create new project

## create new external network

    openstack project create --domain users demo3
    openstack user create --domain users --password pass01 demo3
    openstack role add  --user demo3 --user-domain users --project demo3 admin
    
    openstack network create --external --provider-network-type vlan --provider-segment 103  --share --provider-physical-network physnet1 ext3
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


# demo2-openrc
    export OS_AUTH_URL=http://172.16.11.15/openstack-keystone/v3
    export OS_USERNAME=demo2
    export OS_PASSWORD=pass01
    export OS_USER_DOMAIN_NAME=users
    export OS_PROJECT_DOMAIN_NAME=users
    export OS_PROJECT_NAME=demo2
    export OS_AUTH_VERSION=3
    export OS_IDENTITY_API_VERSION=3