# This document provide guideline on how to configured dhcp client 

note
- it is tested on ubuntu linux 22.04

## DHCP server configurationi 
1. install dhcp server package

        sudo apt install -y isc-dhcp-server

2. edit  file /etc/dhcp/dhcpd.conf for IPv4 dhcp server, such as IP Pool

cat << EOF | sudo tee /etc/dhcp/dhcpd.conf
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;

subnet 192.168.120.0 netmask 255.255.255.0 {
}

subnet 192.168.121.0 netmask 255.255.255.0 {
        range 192.168.121.11 192.168.121.100;
        option routers 192.168.121.254;
        option domain-name-servers 8.8.8.8, 8.8.4.4;
}
subnet 192.168.122.0 netmask 255.255.255.0 {
        range 192.168.122.11 192.168.122.100;
        option routers 192.168.122.254;
        option domain-name-servers 8.8.8.8, 8.8.4.4;
}
host vm1kvm2 {
    hardware ethernet 52:54:00:1a:4b:35;
    fixed-address 192.168.121.101;
    option host-name "vm1kvm2";
}
host vm1kvm2 {
    hardware ethernet 52:54:00:8d:51:aa;
    fixed-address 192.168.121.101;
    option host-name "vm1kvm2";
}
EOF

3. Restart dhcp service

        sudo systemctl restart isc-dhcp-server

4. create file /etc/dhcp/dhcpd6.conf for ipv6 dhcp server, such as IP pool

cat << EOF | sudo tee /etc/dhcp/dhcpd6.conf
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
subnet6 fc00:dead:beef:a120::/64 {
}
subnet6 fc00:dead:beef:a121::/64 {
        range6 fc00:dead:beef:a121::1000:10ff fc00:dead:beef:a121::1000:ffff;
}
subnet6 fc00:dead:beef:a122::/64 {
        range6 fc00:dead:beef:a122::1000:10ff fc00:dead:beef:a122::1000:ffff;
}
host vm1kvm2 {
    hardware ethernet 52:54:00:8d:51:aa;
    # option dhcp6.client-id 00:03:00:01:52:54:00:1a:4b:35;
    fixed-address6 fc00:dead:beef:a121::1000:a101;
}
EOF


5. Restart dhcpv6 service

        sudo systemctl restart isc-dhcp-server6

## DHCP client configuration (Ubuntu linux 22.04)
1. Create file /etc/systemd/system/dhclient6.service, with the following content

        [Unit]
        Description=dhclient for sending DUID IPv6
        Wants=network.target
        Before=network.target

        [Service]
        Type=forking
        ExecStart=/usr/sbin/dhclient -6 -v enp1s0

        [Install]
        WantedBy=multi-user.target

2. Or run the following script

       cat << EOF | sudo tee /etc/systemd/system/dhclient6.service
       [Unit]
       Description=dhclient for sending DUID IPv6
       Wants=network.target
       Before=network.target

       [Service]
       Type=forking
       ExecStart=/usr/sbin/dhclient -6 -v enp1s0

       [Install]
       WantedBy=multi-user.target
       EOF

3. Enable dhclient6 service

       sudo systemctl enable dhclient6.service
       sudo systemctl start dhclient6.service



## configuring DHCP client on Debian 12 to allow dhcp on ipv4 and ipv6 (manual configuration)

1. Move files from directory /run/systemd/network/ to /etc/systemd/network

       mv /run/systemd/network/* /etc/systemd/network

2. Edit file /etc/systemd/network/*.network, and change the following
 - under section **[Network]**, change **DHCP=ipv4** to **DHCP=yes**
 - add new secion **[DHCPv6]** with the following entry  **WithoutRA=solicit** and **DUIDType=link-layer**

       [Network]
       DHCP=yes

       [DHCPv6]
       WithoutRA=solicit
       DUIDType=link-layer

3. Reboot the node

## configuring DHCP client on Debian 12 to allow dhcp on ipv4 and ipv6 (configuration through cloud-init)
1. Create a new cloud-init cdrom/iso, on the hypervisor

       mkdir cdrom
       cd cdrom 
       cat << EOF | tee user-data
       #cloud-config
       password: pass01
       chpasswd: { expire: False }
       ssh_pwauth: True
       runcmd:
        - mv /run/systemd/network/* /etc/systemd/network/
        - sed -i -e "s/DHCP=ipv4/DHCP=yes/" /etc/systemd/network/10-netplan-enp1s0.network
        - echo "[DHCPv6]" | tee -a /etc/systemd/network/10-netplan-enp1s0.network
        - echo "WithoutRA=solicit" | tee -a /etc/systemd/network/10-netplan-enp1s0.network
        - echo "DUIDType=link-layer" | tee -a /etc/systemd/network/10-netplan-enp1s0.network
        - systemctl restart systemd-networkd
       EOF

       cat << EOF | tee meta-data
       instance-id: iid-local01;
       EOF

       genisoimage -output ../seed_debian.iso -volid cidata -joliet -rock user-data meta-data

2. boot vm with debian 12 using the new cloud-init cdrom created on previous step.










