# This document provide information on lab exercise

## Using backup configuration

You can start exploring by configuring the Apstra software, or you can restore the backup configuration that I have created and start from there.

### Restoring Apstra configuration

you can find the backup database of my configuration [here](aos_backup.tgz).

Upload [this file](aos_backup.tgz) into Apstra server, extract it, and restore the database. 

Please refer to [the documentation  ](https://www.juniper.net/documentation/us/en/software/apstra/apstra4.0.0/controller_management.html#restoring-database) on how to restore the database.


### Restoring network configuration for BMS

For the network configuration of the BMS, you can find the archive of the network configuration in [this directory](host/).

Run [script](hosts/restore_network_config.sh) to restore configuration for each BMS in the lab

### Restoring network configuration for other junos devices
in the lab, there are few junos devices which are not managed by apstra, such as PE1, PE2, P1, and ext1.

[PE1](junos/pe1.conf), [P1](junos/p1.conf), [PE2](junos/pe2.conf) : provide ip network connection between DC1 and DC2

[ext1](junos/ext1.conf) : external router that provide connection to external network from datacenter fabric

To upload configuration into junos devices (PE1, PE2, P1, ext1), you can use the [ansible playbook](ansible/upload_config.yaml) 

    cd ansible 
    ansible-playbook ./upload_config.yaml

[gw](gw/bgpd.conf) : gateway that provide connection to internet (it is linux router with FRR routing software)

