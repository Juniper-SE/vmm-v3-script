# Running linux with CRPD as ip router

1. Install linux (ubuntu 22.04 or debian 11)
2. If ubuntu 22.04 is used, verify that package **linux-modules-extra--<version>** are installed. this modules contains mpls kernel modules
3. Install crio container engine, podman and lldp. 
4. Use this script [install_crio.sh](linux/install_crio.sh) to install the packages. Edit the script to match the linux distribution used and CRIO version. Run install_crio.sh on linux to install the packages
5. Upload file [rc.local](linux/rc.local), [config_linux.sh](linux/config_linux.sh), and [install_crdp.sh]() into the linux box.
5. On linux, run script [config_linux.sh](linux/config_linux.sh) to configure the linux for crpd, enable ip routing, and change port of the sshd server on linux.
6. Edit network interface configuration. on ubuntu, they are files under  directory /etc/netplan/, on debian, there are files under /etc/network/interfaces.d
7. For example, this is the network interface configuration for ubuntu

        ubuntu@pe3:~$ cat /etc/netplan/01_net.yaml 

        network:
        ethernets:
            eth0:
            dhcp4: false
            addresses: [ 172.16.10.203/24 ]
            eth1:
            dhcp4: false
            eth2:
            dhcp4: false
            mtu: 9000
            addresses: [ 10.100.1.132/31, 0::ffff:10.100.1.132/127 ]
            eth3:
            dhcp4: false
            mtu: 9000
            addresses: [ 10.100.1.134/31, 0::ffff:10.100.1.134/127] 
        vlans:
            eth1v1:
            dhcp4: false
            addresses: [192.168.255.4/31, 2001:dead:beef:ffff::ffff:4/127]
            link: eth1
            id: 1

        ubuntu@pe3:~$ 

8. For example, this is the network interface configuration for debian

        debian@pe4:~$ cat   /etc/network/interfaces.d/01_net 

        auto lo
        iface lo inet loopback
        auto eth0
        iface eth0 inet static
        address 172.16.10.204/24
        auto eth1
        iface eth1 inet manual
        auto eth2
        iface eth2 inet static
        address 10.100.1.149/31
        mtu 9000
        auto eth3
        iface eth3 inet static
        address 10.100.1.151/31
        mtu 9000

        auto eth1v1
        iface eth1v1 inet static
        address 192.168.255.6/31
        pre-up ip link add link eth1 name eth1v1 type vlan id 1
        post-down ip link del dev eth1v1

        iface eth1v1 inet6 static
        address 2001:dead:beef:ffff::ffff:6/127
        debian@pe4:~$ 

9. Activate the interface configuration

10. Download cRPD image into linux 

        curl -O -L "https://<server>/crpd_file"
11. Load the cRPD image into linux

        sudo podman image load -i <crpd_file.tgz>
        sudo podman image list
12. Run script [install_crpd.sh](linux/install_crpd.sh) to start cRPD container.


# Note 