#!/bin/bash
for i in node{0..3}
do
        ssh ${i}  'sudo sed -i -e "s/^pool/#pool/g" /etc/chrony/chrony.conf; sudo systemctl restart chrony; chronyc sources'
done
