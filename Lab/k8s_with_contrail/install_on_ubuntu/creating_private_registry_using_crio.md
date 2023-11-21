# Creating private registry using CRIO
1. Upload file [install_crio_podman.sh](./install_crio_podman.sh) and [run_registry.sh](./run_registry.sh) into node **registry**
2. Open ssh session into node **registry** and install CRI and podman using script [install_crio_podman.sh](./install_crio_podman.sh)
3. create home directory for the registry, for example ~/registry
4. create directory for certificates, for example ~/registry/certs
5. create directory for data , for example ~/registry/data

        mkdir -p ~/registry/certs
        mkdir -p ~/registry/data

6. edit file sudo vi /etc/ssl/openssl.cnf and add the following (if 172.16.14.10 is not used as IP address of vm **registry**, then change it accordingly)

        [ v3_ca ]
        subjectAltName=IP:172.16.14.10

5. create self signed certificate. use the following script. You can fill anything for the field, except for "Common Name", you have to put the ip address of the VM where the registry is running, in this case 172.16.14.10

        openssl req -newkey rsa:4096 -nodes -sha256 -keyout /home/ubuntu/registry/certs/registry.key -x509 -days 365 -out /home/ubuntu/registry/certs/registry.crt

6. Run script [run_registry.sh](./run_registry.sh) to run the local repository
7. verify that local registry is running using the command 

        podman ps -a

8. make directory /etc/containers/certs.d/172.16.14.10:5000/
9. copy file /home/ubuntu/registry/certs/registry.crt into /etc/containers/certs.d/172.16.14.10:5000/ca.crt

        sudo mkdir -p /etc/containers/certs.d/172.16.14.10:5000/
        sudo cp /home/ubuntu/registry/certs/registry.crt /etc/containers/certs.d/172.16.14.10:5000/ca.crt

# Copy registry certificate to all kubernetes nodes
1. copy registry certificate, in this case /home/ubuntu/registry/certs/registry.crt to all kubernetes nodes as ca.crt
2. on the kubernetes master, create the following directory /etc/docker/certs.d/172.16.14.10:5000
3. copy file registry.crt into directory /etc/docker/certs.d/172.16.14.10:5000
4. repeat step 8 and 9 on all kubernetes node

        #!/bin/bash
        for i in master node{1..3}
        do
                scp /home/ubuntu/registry/certs/registry.crt ${i}:~/
                ssh ${i} "sudo mkdir  -p /etc/docker/certs.d/172.16.14.10:5000; sudo cp ~/registry.crt /etc/docker/certs.d/172.16.14.10:5000/ca.crt"
                # ssh ${i} "sudo mkdir  -p /etc/containers/certs.d/172.16.14.10:5000; sudo cp ~/registry.crt /etc/containers/certs.d/172.16.14.10:5000/ca.crt"
        done


