#!/bin/bash
echo "uploading bgpd.conf into node gw"
scp bgpd.conf gw:~/
echo "restart frr service on node gw"
ssh gw "sudo rm /etc/frr/bgpd.conf; sudo cp bgpd.conf /etc/frr/bgpd.conf; sudo chown frr:frr /etc/frr/bgpd.conf; sudo systemctl restart frr"

