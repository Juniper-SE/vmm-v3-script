#!/bin/bash
VERSION=5.4.0-90
sudo apt install -y linux-image-${VERSION}-generic linux-headers-${VERSION}
sudo sed -i -e 's/1/0/g' /etc/apt/apt.conf.d/10periodic
sudo apt -y update && sudo apt -y upgrade 
grep -A100 submenu  /boot/grub/grub.cfg | grep menuentry 
