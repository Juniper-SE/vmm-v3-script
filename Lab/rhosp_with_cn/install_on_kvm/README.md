# director installation 
1. install RHEL 8.4
2. Run the following script to initialized the director

        sudo useradd stack
        echo "stack ALL=(root) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/stack
        sudo chmod 0440 /etc/sudoers.d/stackk
        sudo hostnamectl set-hostname director.irzan.com
        cat << EOF | sudo tee  /etc/sysconfig/network-scripts/ifcfg-eth0
        TYPE=Ethernet
        PROXY_METHOD=none
        BROWSER_ONLY=no
        BOOTPROTO=none
        DEFROUTE=yes
        IPV4_FAILURE_FATAL=no
        IPV6INIT=yes
        IPV6_AUTOCONF=yes
        IPV6_DEFROUTE=yes
        IPV6_FAILURE_FATAL=no
        NAME=eth0
        DEVICE=eth0
        ONBOOT=yes
        IPADDR=10.1.1.201
        PREFIX=24
        GATEWAY=10.1.1.1
        DNS1=192.168.10.1
        EOF
        sudo passwd stack
        sudo reboot

3. install redhat subscription 

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

4. Install command line tools for director installation and configuration

        ssh stack@director
        sudo dnf install -y python3-tripleoclient

5. Create directory for the installation images

        mkdir ~/images
        mkdir ~/templates

6. Generate the default container image preparation file

        sudo openstack tripleo container image prepare default \
        --local-push-destination \
        --output-env-file containers-prepare-parameter.yaml

7. Edit file containers-prepare-parameter.yaml, and add the following

    parameter_defaults:
        ContainerImagePrepare:
        - push_destination: true
        excludes:
            - ceph
            - prometheus
        ...
        ...
            neutron_driver: null
        ...
        ...
        tag_from_label: '{version}-{release}'
        ContainerImageRegistryCredentials:
          registry.redhat.io:
            userlogin: password
8. Copy undercloud.conf into home directory

        cp \
        /usr/share/python-tripleoclient/undercloud.conf.sample \
        ~/undercloud.conf

9. edit file undercloud.conf and add the following entries

        [DEFAULT]
        container_images_file = /home/stack/containers-prepare-parameter.yaml
        generate_service_certificate = false
        local_interface=eth1
        overcloud_domain_name = irzan.com
        local_ip=10.1.101.201/24
        cidr=10.1.101.0/24
        dhcp_end = 10.1.101.150
        dhcp_start = 10.1.101.50
        gateway=10.1.101.1
        inspection_iprange=10.1.101.160-10.1.101.200

10. Run the following command to install director on the undercloud:

        tmux
        openstack undercloud install

