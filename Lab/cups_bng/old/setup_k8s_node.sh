#!/bin/bash
sudo sed -i -e 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd
sudo mkdir /root/.ssh
sudo cp /home/ubuntu/.ssh/* /root/.ssh
sudo apt -y install python3-pip
sudo ln -s /usr/bin/pip3 /usr/bin/pip

