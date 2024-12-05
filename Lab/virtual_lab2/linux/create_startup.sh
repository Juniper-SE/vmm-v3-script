#!/bin/bash
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

sudo cp rc.local /etc/rc.local
sudo chmod +x /etc/rc.local
sudo chmod +x /etc/systemd/system/rc-local.service 
sudo systemctl enable rc-local.service
sudo systemctl start rc-local.service
