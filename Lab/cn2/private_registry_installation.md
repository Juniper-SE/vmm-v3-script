# installing/creating private registry

1. upload file [install_crio.sh](install_crio.sh) into node **registry**

        scp install_crio.sh registry:~/

2. ssh into node **registry**, and update the base OS 

        tmux
        sudo apt -y update
        sudo apt -y upgrade
        sudo reboot

3. ssh into node **registry** and run script install_crio.sh to install CRI-O container engine. 

        tmux
        sudo ./install_crio.sh

3. On node **registry**, create home directory for the registry, for example ~/registry
4. On node **registry**, create directory for certificates, for example ~/registry/certs
5. On node **registry**, create directory for data , for example ~/registry/data

        mkdir -p ~/registry/certs
        mkdir -p ~/registry/data

8. edit file sudo vi /etc/ssl/openssl.cnf and add the following 

        sudo vi /etc/ssl/openssl.cnf
        [ v3_ca ]
        subjectAltName=IP:172.16.14.10
        # 172.16.14.10 is the ip address of VM registry. If the VM is using different IP address, then set it accordingly

9. create self signed certificate. use the following script. You can fill anything for the fields, except for "Common Name", you have to put the ip address of the VM where the registry is running, for example 172.16.14.10

        openssl req -newkey rsa:4096 -nodes -sha256 -keyout ~/registry/certs/registry.key -x509 -days 365 -out ~/registry/certs/registry.crt


10. Upload script [run_registry.sh](./run_registry.sh) to VM **registry**, and run the script to start the registry container

        podman run --name registry \
                -p 5000:5000 \
                -v ~/registry/data:/var/lib/registry \
                -v ~/registry/certs:/certs \
                -e "REGISTRY_HTTP_TLS_CERTIFICATE=/certs/registry.crt" \
                -e "REGISTRY_HTTP_TLS_KEY=/certs/registry.key" \
                --network podman \
                -d registry:2


11. On node **registry** make directory /etc/containers/certs.d/172.16.14.10:5000/ . If the VM is using ip address other than 172.16.14.10, then change it accordingly.

12. copy file ~/certs/registry.crt into /etc/containers/certs.d/172.16.14.10:5000/ca.crt

        sudo mkdir -p /etc/containers/certs.d/172.16.14.10:5000/
        sudo cp certs/registry.crt /etc/containers/certs.d/172.16.14.10:5000/ca.crt

## For container enginer, CRIO, Copy registry certificate to all kubernetes nodes
1. copy registry certificate from node **registry** , in this case ~/registry/certs/registry.crt to all kubernetes nodes
2. on the kubernetes master, create the following directory /etc/containers/certs.d/172.16.14.10:5000 (or /etc/container/certs.d/172.16.14.10:5000)
3. copy file registry.crt into  /etc/docker/certs.d/172.16.14.10:5000/ca.crt (or /etc/container/certs.d/172.16.14.10:5000/ca.crt)
4. repeat step 1-33 on all kubernetes node. Or you can use the following script to do step 1-3

        #!/bin/bash
        # 172.16.14.10 is the ip address of the registry 
        REGISTRY_IP=172.16.14.10
        for i in node{0..3}
        do
                scp certs/registry.crt ${i}:~/
                ssh ${i} "sudo mkdir  -p /etc/containers/certs.d/${REGISTRY_IP}:5000; sudo cp ~/registry.crt /etc/containers/certs.d/${REGISTRY_IP}:5000/ca.crt" 
        done

## For container enginer, containerd , Copy registry certificate to all kubernetes nodes
1. copy registry certificate from node **registry** , in this case ~/registry/certs/registry.crt to all kubernetes nodes
2. on the kubernetes master, copy the certificate to directory /etc/ssl/certs
3. restart containerd services or reboot the kubernetes node.
4. repeat step 1-3 on all kubernetes node. Or you can use the following script to do step 1-3

        #!/bin/bash
        # 172.16.14.10 is the ip address of the registry 
        # REGISTRY_IP=172.16.14.10
        for i in node{0..3}
        do
                scp certs/registry.crt ${i}:~/
                ssh ${i} "sudo cp ~/registry.crt /etc/ssl/certs/" 
        done

## running registry container as service
1. run the following script to create systemd's registry service

        podman generate systemd --new --name registry | sudo tee /etc/systemd/system/registry.service
        sudo systemctl enable registry

2. Stop and remove the existing registry container

        podman stop registry 
        podman rm registry

3. Start systemd registry service

        sudo systemctl start registry
