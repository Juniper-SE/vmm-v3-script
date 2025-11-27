# initialize LXD

    sudo lxd init

# download alpine LXC image and create lxc alpine

    lxc image copy images:alpine/edge local: --alias alpine
    lxc launch alpine client
    lxc exec client sh
    apk add merge-usr
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

    export LXC=cl4-cust2
    export OVS=pe4ge0
    export IPV4=192.168.110.4/24
    export GW4=192.168.110.254
    export IPV6=fc00:Dead:beef:110::1000:4/64
    export GW6=fc00:Dead:beef:110::1
    export VLAN=1002

    #!/bin/bash
    # create client LXC with VLAN
    
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


    export LXC=cl1ce4-cust2
    export OVS=ce4_cust2_eth1
    export IPV4=192.168.114.2/24
    export GW4=192.168.114.1
    export IPV6=fc00:Dead:beef:114::1000:1/64
    export GW6=fc00:Dead:beef:114::1

    #!/bin/bash
    # create client LXC without VLAN
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


# creater router lxc 

    lxc copy client router
    lxc start router
    lxc exec router sh
    apk add frr
    sed -i -e "s/bgpd=no/bgpd=yes/" /etc/frr/daemons
    rc-update add sshd
    lxc stop router

# create router

    export CUST=cust2
    export LAN=eth1
    for i in ce2 ce3 ce4
    do
        export BR=${i}_${CUST}_${LAN}
        sudo ip link add dev $BR type bridge
        sudo ip link set dev $BR up
    done

# create router (with vlan)

    export LXC=ce4-cust2
    export OVS=pe4ge3
    export IPV4WAN=192.168.255.3/31
    export IPV6WAN=fc00:Dead:beef:ffff::3/127
    export IPV4LAN=192.168.114.1/24
    export IPV6LAN=fc00:Dead:beef:114::1/64
    export VLAN=1002
    export LAN=ce4_cust2_eth1
    export ASN=4200002004
    export ASN_PEER=4200000001
    export IPV4PEER=192.168.255.2
    export IPV6PEER=fc00:dead:beef:ffff::2
    export NETWORKV4=192.168.114.0/24
    export NETWORKV6=fc00:Dead:beef:114::/64



    #!/bin/bash
    # create client LXC with VLAN
    echo "create router ${LXC} "
    lxc copy router ${LXC}
    echo "changing container ${LXC}"
    lxc query --request PATCH /1.0/instances/${LXC} --data "{
        \"devices\": {
            \"eth0\" :{
                \"name\": \"eth0\",
                \"nictype\": \"bridged\",
                \"parent\": \"${OVS}\",
                \"vlan\" : \"${VLAN}\",
                \"type\": \"nic\"
            },
            \"eth1\" :{
                \"name\": \"eth1\",
                \"nictype\": \"bridged\",
                \"parent\": \"${LAN}\",
                \"type\": \"nic\"
            }
        }
    }"

    echo "changing containers${LXC}"
    cat << EOF | tee interfaces
    auto eth0
    iface eth0 inet static
        address $IPV4WAN
        mtu 1500
    iface eth0 inet6 static
        address $IPV6WAN
    auto eth1
    iface eth1 inet static
        address $IPV4LAN
        mtu 1500
    iface eth1 inet6 static
        address $IPV6LAN
    EOF
    echo "push configuration into node ${LXC}"
    lxc file push interfaces  ${LXC}/etc/network/interfaces
    echo "frr configuration" 
    cat << EOF | tee frr.conf
    router bgp $ASN
        no bgp ebgp-requires-policy
        neighbor $IPV4PEER remote-as ${ASN_PEER}
        neighbor $IPV6PEER remote-as ${ASN_PEER}
        !
        address-family ipv4 unicast
            network $NETWORKV4
        exit-address-family
        !
        address-family ipv6 unicast
            network $NETWORKV6
            neighbor $IPV6PEER activate
        exit-address-family
    exit
    EOF
    echo "push configuration into node ${LXC}"
    lxc file push frr.conf ${LXC}/etc/frr/frr.conf
    echo "net.ipv6.conf.all.forwarding=1" > ipv6.conf
    lxc file push ipv6.conf ${LXC}/etc/sysctl.d/ipv6.conf
    lxc start ${LXC}

    sysctl -p /etc/sysctl.d/ipv6.conf

