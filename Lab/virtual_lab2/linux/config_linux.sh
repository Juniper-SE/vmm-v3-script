#!/bin/bash
echo Creating linux configuration
echo "############################"

cp /etc/sysctl.conf ~/
cp /etc/ssh/sshd_config ~/
cat << EOF | sudo tee /etc/systemd/system/rc-local.service 
[Unit]
 Description=/etc/rc.local Compatibility
 ConditionPathExists=/etc/rc.local


[Service]
 Type=forking
 ExecStart=/etc/rc.local start
 TimeoutSec=0
 StandardOutput=tty
 RemainAfterExit=yes
 SysVStartPriority=99


[Install]
 WantedBy=multi-user.target
EOF


sudo chmod +x /etc/systemd/system/rc-local.service 
sudo systemctl enable rc-local.service


LN=`grep -n 'Port 22' /etc/ssh/sshd_config | cut -d ':' -f 1`
if [ -z "${LN}" ];
then
        echo "nothing on the config"
else
        echo "deleting config, from line ${LINENUM}"
        sudo sed -i -e "${LN}d" /etc/ssh/sshd_config
fi

echo "Port 8022" | sudo tee -a /etc/ssh/sshd_config 


sudo systemctl restart sshd

LN=`grep -n 'net.ipv4.ip_forward' /etc/sysctl.conf | cut -d ':' -f 1`

if [ -z "${LN}" ];
then
        echo "nothing on the config"
else
        echo "deleting config, from line ${LINENUM}"
        sudo sed -i -e "${LN}d" /etc/sysctl.conf
fi


LN=`grep -n "net.ipv6.conf.all.forwarding" /etc/sysctl.conf | cut -d ":" -f 1`
if [ -z "${LN}" ];
then
        echo "nothing on the config"
else
        echo "deleting config, from line ${LINENUM}"
        sudo sed -i -e "${LN}d" /etc/sysctl.conf
fi

cat << EOF | sudo tee -a /etc/sysctl.conf
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
EOF


sudo sysctl -f /etc/sysctl.conf

sudo cp rc.local /etc/rc.local
sudo chmod +x /etc/rc.local




