#!/bin/bash

cat << EOF  | sudo tee /etc/netplan/01-netcfg.yaml
network:
    version: 2
    # renderer: networkd
    ethernets:
        eth0:
            dhcp4: false
            addresses: [ 172.16.10.3/24]
            gateway4: 172.16.10.1
            nameservers:
                addresses: [ 8.8.8.8, 8.8.4.4 ]
EOF

cat << EOF | sudo tee /containers_data/status/app/aos.conf
{
    "ip": "172.16.10.2",
    "user": "ztp",
    "password": "J4k4rt4#01"
}
EOF

cat << EOF | sudo tee /containers_data/tftp/junos_custom1.sh
#!/bin/sh 
cli -c "configure; set system commit synchronize; set chassis evpn-vxlan-default-switch-support; commit and-quit"
EOF

cat << EOF | sudo tee /containers_data/tftp/junosevo_custom1.sh
#!/bin/sh 
cli -c "configure; set forwarding-options tunnel-termination; commit and-quit"
EOF


sudo chmod +x /containers_data/tftp/junos_custom1.sh
sudo chmod +x /containers_data/tftp/junosevo_custom1.sh


sudo grep -n "Step"  /containers_data/dhcp/dhcpd.conf
sudo sed -i -e '9,29d' /containers_data/dhcp/dhcpd.conf
sudo sed -i -e 's/dc1.yourdatacenter.com/vmmlab.juniper.net/' /containers_data/dhcp/dhcpd.conf
sudo grep -n "name-server" /containers_data/dhcp/dhcpd.conf
sudo sed -i -e 's/10.1.2.13, 10.1.2.14/8.8.8.8,8.8.4.4/' /containers_data/dhcp/dhcpd.conf

cat ~/ztp_config.txt | sudo tee -a  /containers_data/dhcp/dhcpd.conf


line1=`grep -n "Step 2"  /containers_data/dhcp/dhcpd.conf | cut -f 1 -d ":"`
line1=`expr $line1 + 1`
line2=`grep -n "Step3"  /containers_data/dhcp/dhcpd.conf | cut -f 1 -d ":"`
line2=`expr $line2 - 1`
sed -i -e "${line1},${line2}d" /containers_data/dhcp/dhcpd.conf
sed -i -e 's/dc1.yourdatacenter.com/vmmlab.juniper.net/' /containers_data/dhcp/dhcpd.conf
sed -i -e 's/10.1.2.13, 10.1.2.14/8.8.8.8,8.8.4.4/' /containers_data/dhcp/dhcpd.conf



