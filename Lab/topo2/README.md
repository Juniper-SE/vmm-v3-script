# Lab topo2

## nodes in the topology 

- pe1, pe2, pe3, pe4, pe5, p1, p2, p3, p4, p5: vJunosrouter
- client: ubuntu VM to simulate client or ce
- crpd: ubuntu VM to host cRPD software
- nms1, nms2 : ubuntu VM to host nms application
- br1, br2, br3: alpine VM to simulate delay and link failure between vJunosNode


## Topology

Connection between nodes
![topology](topology.webp)

## Deploying the topology 

Screenshot recording for this can be found [here]()

1. go into the **topo1** directory 

       cd ~/git/vmm-v3-script/Lab/topo2

2. upload the topology into VMM

       ../../vmm.py upload

3. start the topology 

       ../../vmm.py start

4. wait for few minutes until node **gw** is up and running
5. upload configuration into node **gw**

       ../../vmm.py set_gw

6. wait for few minutes until the ZTP process for all vjunos node are up and running
7. open ssh session into node **gw**, test connectivity to vjunos node (r1, r2, r3, r4) and open ssh session, or test connectivity to junos VM from your workstation.

       ssh gw
       ping pe1
       ssh admin@pe1

8. return to your workstation, and upload configuration into Linux VM :  **client**, **crpd**, **nms1**, **nms2**, **br1**, **br2**, **br3**

       ../../vmm.py set_host

9. open ssh session into node client1 to verify that it is up and running

       ssh client1
       ip addr show 

10. Run ansible playbook [upload_nodes.yaml](setup/host/update_nodes.yaml) to update software on linux VM and upload the necessary script.

       cd setup/host
       ansible-playbook update_nodes.yaml

11. Reboot the linux VMs node (client, nms1, nms2, crpd, br1, br2, br3 using script [reboot_vm.sh](setup/host/reboot_vm.sh))

## Installing Juniper CRPD container on node crpd

1. Upload script [install_crpd.sh](setup/host/install_crpd.sh) into node **crpd**

       scp ./install_crpd.sh crpd:~/

2. Upload crpd software into node **crpd** and load it using podman

       scp junos-routing-crpd-amd64-25.2R1.9.tgz crpd:~/
       ssh crpd
       sudo podman load -i junos-routing-crpd-amd64-25.2R1.9.tgz 
       sudo podman image ls
       
3. Run script [install_crpd.sh](setup/router/install_crpd.sh)  on node **crpd** to create container crpd

       ./install_crpd.sh crpd 25.2R1.9
       sudo podman ps -a 

4. Access crpd container and insert the initial configuration [crpd_initial.conf](setup/router/crpd_initial.conf)

       sudo podman exec -it crpd cli
       

5. Verify that isis adjacency has been established and crpd receive isis routes

       show isis adj
       show route protocol isis


## Upload additional configuration into vJunosRouter nodes

Screenshot recording for this can be found [here](https://asciinema.org/a/738391)

1. use ansible playbook [set_intf.yaml](setup/set_intf.yaml) to upload additional configuration (setting ip on interface ge-0/0/0 or et-0/0/0)

       cd ~/git/vmm-v3-script/Lab/topo2/setup/router
       ansible-playbook set_bgp.yaml

2. open ssh session into **pe1** to verify that configuration is working (BGP session between PE1/2/3/4/5 and crpd has been established)

       ssh pe1
       show configuration 
       show bgp summary

## create linux container to simulate client on node client1

Screenshot recording for this can be found [here](https://asciinema.org/a/738393)

1. upload script [create_client.sh](set/create_client.sh) into node client1

       scp ~/git/vmm-v3-script/Lab/topo1/setup/create_client.sh

2. initialize lxd on node client1 (answer all the question with default parameter)

3. open ssh session into node client1, and download alpine LXC image, and create an lxc container called client

       ssh client1
       lxc image copy images:alpine/edge local: --alias alpine
       lxc launch alpine client
       lxc ls

4. access container client, and add packages openssh and iperf

       lxc exec client sh
       apk update
       apk upgrade
       apk add openssh iperf

5. configure openssh to allow root login and set root password

       passwd root
       cat << EOF | tee -a /etc/ssh/sshd_config
       PermitRootLogin yes
       EOF
       rc-update add sshd
       service sshd start
       ssh root@localhost

5. exit from the shell of container client and stop the container

       exit
       lxc stop client

6. Run script  [create_client.sh](set/create_client.sh) to create multiple client to simulate users on r1, r2, r3, r4

       ./create_client.sh
       lxc ls

7. Access the simulated client and test connectivity to other client accross the network

       lxc exec c11 sh 
       ping 192.168.20.1
       ping 192.168.30.1
       ssh root@fc00:dead:beef:aa30::1000:1



