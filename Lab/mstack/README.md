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

# creating flavor
    openstack flavor create --public --vcpus 1 --ram 128 --disk 1 m1.tiny   
    openstack flavor create --public --vcpus 1 --ram 2048 --disk 10 m1.small 
    openstack flavor create --public --vcpus 2 --ram 4096 --disk 40 m1.medium
    openstack flavor create --public --vcpus 2 --ram 8192 --disk 60 m1.large


# create external network

    openstack network create --external --provider-network-type vlan --provider-segment 101  --provider-physical-network physnet1 ext1
    openstack subnet create --gateway 172.16.101.1  --subnet-range 172.16.101.0/24 --network ext1 ext1_subnet



# error message

OpenStack services are exposed via virtual IP addresses. This range should contain at least ten addresses and must not overlap with external
network CIDR. To access APIs from a remote host, the range must reside within the subnet that the primary network interface is on.
On multi-node deployments, the range must be addressable from all nodes in the deployment.
OpenStack APIs IP ranges (172.16.1.201-172.16.1.240): 172.16.11.11-172.16.11.60
Comma separated list of devices to be used by Ceph OSDs. `/dev/disk/by-id/<id>` are preferred, as they are stable given the same device.
Ceph devices (/dev/disk/by-id/scsi-SATA_QEMU_HARDDISK_QM00002): /dev/sdb
Node has been bootstrapped with roles: storage, control, compute
Task was destroyed but it is pending!
task: <Task pending name='Task-2924' coro=<Connection._pinger.<locals>._do_ping() running at /snap/openstack/743/lib/python3.12/site-packages/juju/client/connection.py:517> wait_for=<Future pending cb=[Task.task_wakeup()]> cb=[create_task_with_handler.<locals>._task_result_exp_handler(task_name='tmp', logger=<Logger juju....ction (ERROR)>)() at /snap/openstack/743/lib/python3.12/site-packages/juju/_jasyncio.py:32]>