# How setup the vMX as WAG
## topology
This is the topology of the lab
![topology](images/topology.png)

## Devices in the lab

- VMX : access (access switch (for vlan)), vBNG as WAG 
- CP : radius server, database (MySQL), Portal (Flask)
- webserver 


## Credential to access devices
- Ubuntu linux
    - user: ubuntu
    - password: pass01
- JUNOS VM
    - user: admin
    - password: pass01

## To create the lab topology and initial configuration of VMs
1. Go to directory [wag](./)
2. Edit file [lab.yaml](./lab.yaml). Set the following parameters to choose which vmm server that you are going to use and the login credential:
    - vmmserver 
    - jumpserver
    - user 
    - adpassword
    - ssh_key_name ( please select the ssh key that you want to use, if you don't have it, create one using ssh-keygen and put it under directory **~/.ssh/** on your workstation )
3. If you want to add devices or change the topooogy of the lab, then edit file [lab.yaml](lab.yaml)
4. use [vmm.py](../../vmm.py) script to deploy the topology into the VMM. Run the following command from terminal

        ../../vmm.py upload  <-- to create the topology file and the configuration for the VMs and upload them into vmm server
        ../../vmm.py start   <-- to start the topology in the vmm server


5. Verify that you can access node **gw** using ssh (username: ubuntu,  password: pass01 ). You may have to wait for few minutes for node **gw** to be up and running
6. Run script [vmm.py](../../vmm.py) to send and run initial configuration on node **gw**

        ../../vmm.py set_gw

7. Verify that you can access other nodes (linux and junos VM), such **cp** and **webserver**, etc. Please use the credential to login.

        ssh cp

8. Run script [vmm.py](../../vmm.py) to send and run initial configuration on linux nodes. This script will also reboot the VM. So wait before you test connectivity into the VM

        ../../vmm.py set_host

9. Verify that you can access linux and junos VMs, such **cp** and **webserver**, without entering the password. You may have to wait for few minutes for the nodes to be up and running

        ssh webserver
        ssh cp

## update system and install server application on node ubuntu nodes
1. use ansible script [update_System.yaml](linux_node/update_system.yaml) to update system and install the necessary software, such as freeradius and mariadb server

## edit initial setup of mariadb server and load freeradius table into sql server

1. open ssh session into node **cp**

        ssh cp

2. initialize mariadb server

        sudo mysql_secure_installation

3. Restart mariadb server

        sudo systemctl restart mariadb

4. using mysql client, create database radius

        sudo mysql -u root -p
        show databases;
        create database radius;
        show databases;
        exit

5. Load freeradius schema database into mariadb 

        sudo -s
        cd /etc/freeradius/3.0/mods-config/sql/main/mysql
        mysql -u root -p radius < schema.sql
        mysql -u root -p radius < setup.sql

6. by default, the schema will set column nasportid on table radacct to varchar(15). This may not be enough, so the data type need to be modified. Run the following command through mysql client

        mysql -u radius -p radius
        alter table radacct modify nasportid varchar(32);

6. Test access into mariadb server using user radius, password radpass

        mysql -u radius -p radius

## configure freeradius to use mariadb
1. enable sql on freeradius 

        ssh cp
        sudo ln -s /etc/freeradius/3.0/mods-available/sql /etc/freeradius/3.0/mods-enabled/sql

2. edit file /etc/freeradius/3.0/mods-enabled/sql, and change the following configuration

        sudo vi /etc/freeradius/3.0/mods-enabled/sql

   - set dialect to "mysql"
   - set driver to "rlm_sql_${dialect}"
   - under mysql -> tls, comment out the tls configuration (add # at the beginning of the lines for tls configuration)
   - set server to "127.0.0.1"
   - set port to 3306
   - set login to "radius"
   - set password to "radpass"

   you may need to remove the # sign at the beginning of the line
   
   and save the files

3. edit file /etc/freeradius/3.0/sites-enabled/default, and change the following configuration

        sudo vi /etc/freeradius/3.0/sites-enabled/default


   - under section **authorize {**, look for entry **-sql** and remove the minus (-) sign
   - under section **accounting {**, look for entry **-sql** and remove the minus (-) sign
   - under section **accounting {**, look for entry **detail** and add # at the beginning of the line 

4. edit file /etc/freeradius/3.0/sites-enabled/inner-tunnel, and change the following configuration

        sudo vi  /etc/freeradius/3.0/sites-enabled/inner-tunnel


   - under section **authorize {**, look for entry **-sql** and remove the minus (-) sign

5. edit file /etc/freeradius/3.0/clients.conf, and add the following entry into it.

        sudo vi  /etc/freeradius/3.0/clients.conf 

        client wag {
                ipaddr = 172.16.12.2
                secret  = jnpr123
        }

6. edit file /etc/freeradius/3.0/users, delete the existing entry for **DEFAULT** including the radius attribute reply, and add the following entry

        sudo vi /etc/freeradius/3.0/users
        
        DEFAULT    Auth-Type := Accept
                   ERX-Service-Activate:1 += "redirDynamic(http://172.16.13.11)"

7. Restart freeradius server

        sudo systemctl enable freeradius
        sudo systemctl restart freeradius
        sudo systemctl status freeradius

## install flask 

1. install flask 

        sudo apt remove -y python3-click python3-markupsafe python3-jinja2 python3-importlib-metadata 
        sudo apt autoremove -y 
        sudo pip3 install flask flask-mysql

2. create directory ~/webserver, and upload file [webserver.py](webserver/webserver/webserver.py) to it
        
        ssh cp "mkdir ~/webserver"
        scp webserver/webserver/webserver.py cp:~/webserver

3. Run the webserver application 

        tmux
        sudo python3 ~/webserver/webserver.py


## Upload configuration into node WAG and ACCESS

1. Upload configuration into junos node **wag** and **access**. The configuration are available [here](./junos_config). You can also use [ansible playbook](junos_config/upload_config.yaml) to upload the configuration

        cd node_configuration/junos_config
        ansible-playbook upload_config.yaml

6. Node **wag**  may need to be reboot after the configuration has been applied and commited.


## enable BGP on node **gw**
1. open ssh session into node **gw** and install frr software

        sudo apt -y update && sudo apt -y upgrade && sudo apt -y install frr

2. Edit file /etc/frr/daemons, and set **yes** to bgpd

3. Restart frr daemon

        sudo systemctl restart frr

4. open access into FRR routing console
        
        sudo vtysh 

7. add the following configuratino FRR to enable bgp

        enable 
        config t
        router bgp 65100
        neighbor 172.16.12.2 remote-as 65200
        neighbor fc00:dead:beef:1::12:2 remote-as 65200
        !
        address-family ipv4 unicast
        network 0.0.0.0/0
        exit-address-family
        !
        address-family ipv6 unicast
        network ::/0
        neighbor fc00:dead:beef:1::12:2 activate
        exit-address-family
        !
        exit
        exit
        write mem

8. on node **wag** or **gw**, verify that BGP peers are up

9. Now you can explore the WAG lab.
