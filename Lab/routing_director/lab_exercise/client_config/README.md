# initialize LXD

    sudo lxd init

# download alpine LXC image and create lxc alpine

    lxc image copy images:alpine/edge local: --alias alpine
    lxc launch alpine client
    merge-usr
    apk del merge-usr
    apk add openssh
    passwd root
    cat << EOF | tee -a /etc/ssh/sshd_config
    PermitRootLogin yes
    EOF
    rc-update add sshd
    service sshd restart
    exit
    lxc stop client


# create client (with vlan)

    #!/bin/bash
    # create client LXC with VLAN
    LXC=cl1pe1
    OVS=pe1ge0
    IPV4=192.168.101.2/24
    GW4=192.168.101.1
    IPV6=fc00:Dead:beef:A101::1000:1/64
    GW6=fc00:Dead:beef:A101::1
    echo "create client ${LXC} "
    lxc copy client ${LXC}
    echo "changing container ${LXC}"
    lxc query --request PATCH /1.0/instances/${LXC} --data "{
        \"devices\": {
            \"eth0\" :{
                \"name\": \"eth0\",
                \"nictype\": \"bridged\",
                \"parent\": \"${OVS}\",
                \"vlan\" : \"${VLAN}\",
                \"type\": \"nic\"
            }
        }
    }"

    echo "changing containers${LXC}"
    cat << EOF | tee interfaces
    auto eth0
    iface eth0 inet static
        address $IPV4
        gateway $GW4
        mtu 1500
    iface eth0 inet6 static
        address $IPV6
        gateway $GW6
    EOF


    echo "push configuration into node ${LXC}"
    lxc file push interfaces  ${LXC}/etc/network/interfaces
    lxc start ${LXC}

# create client (w/o vlan)

    #!/bin/bash
    # create client LXC without VLAN
    LXC=cl1pe3
    OVS=pe3ge0
    IPV4=192.168.103.2/24
    GW4=192.168.103.1
    IPV6=fc00:Dead:beef:A103::1000:1/64
    GW6=fc00:Dead:beef:A103::1
    echo "create client ${LXC} "
    lxc copy client ${LXC}
    echo "changing container ${LXC}"
    lxc query --request PATCH /1.0/instances/${LXC} --data "{
        \"devices\": {
            \"eth0\" :{
                \"name\": \"eth0\",
                \"nictype\": \"bridged\",
                \"parent\": \"${OVS}\",
                \"type\": \"nic\"
            }
        }
    }"

    echo "changing containers${LXC}"
    cat << EOF | tee interfaces
    auto eth0
    iface eth0 inet static
        address $IPV4
        gateway $GW4
        mtu 1500
    iface eth0 inet6 static
        address $IPV6
        gateway $GW6
    EOF


    echo "push configuration into node ${LXC}"
    lxc file push interfaces  ${LXC}/etc/network/interfaces
    lxc start ${LXC}
