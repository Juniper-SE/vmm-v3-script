# How to create disk image for VMM

This document provides guideline on how to create linux disk image that can be used on juniper VMM.

## Steps.
1. Download the cloud image, such ubuntu cloud image [https://cloud-images.ubuntu.com/](https://cloud-images.ubuntu.com/), centos cloud image [https://cloud.centos.org/centos/](https://cloud.centos.org/centos/), or debian cloud image [https://cloud.debian.org/images/cloud/](https://cloud.debian.org/images/cloud/)
2. Edit the vmm configuration file [make_vm1.conf](make_vm1.conf). Change the necessary parameter.
3. Upload file make_vm1.conf into vmm server
4. Upload the cloud disk image into vmm server
4. upload CDROM image [seed.iso](seed.iso) into vmm server. This CDROM image contains cloud-init file requires to initialize the VM, such setting password
5. open ssh session into vmm server.
6. open session into vmm server.
7. check the default size of the disk image, if it doesn't meet the required disk space, expand the disk size using qemu-img command. Remember resizing the disk image can only be done before the vm started.

        scp seed.iso q-pod25-vmm.englab.juniper.net:~/create/
        scp debian-11-generic-amd64.qcow2 q-pod25-vmm.englab.juniper.net:~/create/
        scp make_vm1.conf q-pod25-vmm.englab.juniper.net:~/create/
        ssh q-pod25-vmm.englab.juniper.net
        cd create
        cp  debian-11-generic-amd64.qcow2 debian.img
        qemu-img info debian.img
        qemu-img resize debian.img 20G
        qemu-img info debian.img

![create1.png](images/create1.png)

8. Stop and unbind any existing topology running on the VMM

        vmm list
        vmm stop
        vmm unbind

9. Do a vmm config on file make_vm1.conf

        vmm config make_vm1.conf -g vmm-default
10. Start the topology

        vmm bind
        vmm start
11. To verify that VM is running, do a vmm list the virtual machines

        vmm list


