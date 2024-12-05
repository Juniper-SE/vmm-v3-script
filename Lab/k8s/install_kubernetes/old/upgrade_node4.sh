#!/bin/bash
sudo apt -y update 
sudo apt -y upgrade
sudo apt -y install nfs-kernel-server
sudo mkdir -p /media/nfsshare
sudo mkdir -p /media/nfsshare/webserver
sudo chown -R nobody:nogroup /media/nfsshare
sudo chmod 777 /media/nfsshare
echo "/media/nfsshare *(rw,sync,no_subtree_check)"  | sudo tee -a /etc/exports
echo "/media/nfsshare/webserver *(rw,sync,no_subtree_check)"  | sudo tee -a /etc/exports

sudo reboot
