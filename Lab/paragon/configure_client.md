
## configure client for site1, site2, site3, site4
there are four sites in the lab, site1 connected to pe11, site2 connected to pe12, site3 connected to pe13, and site4 connected to pe14.

The following steps, we are going to configure clients for site1, site2, site3, and site4. 

The client is using linux container (LXC) running on node **client**

1. open ssh session into node **client**
2. Refresh snap

        sudo snap refresh

3. Initialize LXD

        sudo lxd init

4. Download alpine linux LXC image

        lxc image copy images:alpine/edge local: --alias alpine
        lxc image ls

5. Create two LXC instance

        lxc launch alpine router
        lxc launch alpine client

6. Access LXC client shell, install openssh, add sshd to startup script, and create ssh-key for ssh

        lxc exec client sh
        apk update
        apk upgrade
        apk add openssh
        rc-update add sshd
        service sshd start
        ssh-keygen -t rsa
        cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
        exit
        lxc stop client

7. Access LXC router shell, install frr, dhcp-server and lldpd, add dhcpd and frr to startup script

        lxc exec router sh
        apk update
        apk upgrade
        apk add frr dhcp-server lldpd
        rc-update add dhcpd
        rc-update add frr
        sed -i -e "s/bgpd=no/bgpd=yes/" /etc/frr/daemons
        exit
        lxc stop router
        lxc ls

8. from your workstation, upload scripts [config/client/lxc/create/set_network.sh](config/client/lxc_create/set_network.sh) script [config/client/lxc_create/create_lxc_routing_global.sh](config/client/lxc_create/create_lxc_routing_global.sh) to node **client**, and run those script on node **client**

        scp config/client/lxc_create/create_lxc_routing_global.sh client:~/
        scp config/client/lxc/create/set_network.sh client:~/
        ssh client
        ./set_network.sh
        ./create_lxc_routing_global.sh

9. Multiple LXC instances has been create, and they can be used to test connectivity between sites.


