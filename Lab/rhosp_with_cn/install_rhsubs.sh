#!/usr/bin/env bash
sudo subscription-manager register --username $1 --password $2
POOL_ID=`sudo subscription-manager list --available --all --matches="Red Hat OpenStack" | grep  "Pool ID"  | head -1 | cut -f 2 -d ":" | sed -e 's/^[ \t]*//'`
# sudo subscription-manager list --available --all --matches="Red Hat OpenStack"
sudo subscription-manager attach --pool=${POOL_ID}
sudo subscription-manager release --set=8.4
sudo subscription-manager repos --disable=*
sudo subscription-manager repos \
--enable=rhel-8-for-x86_64-baseos-eus-rpms \
--enable=rhel-8-for-x86_64-appstream-eus-rpms \
--enable=rhel-8-for-x86_64-highavailability-eus-rpms \
--enable=ansible-2.9-for-rhel-8-x86_64-rpms \
--enable=openstack-16.2-for-rhel-8-x86_64-rpms \
--enable=fast-datapath-for-rhel-8-x86_64-rpms
sudo dnf module reset container-tools
sudo dnf module enable -y container-tools:3.0
sudo dnf update -y
sudo reboot
