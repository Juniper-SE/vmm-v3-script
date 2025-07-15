# Creating private registry
1. install docker engine
2. create home directory for the registry, for example ~/registry
3. create directory for certificates, for example ~/registry/certs
4. create directory for data , for example ~/registry/data

        mkdir -p ~/registry/certs
        mkdir -p ~/registry/data

5. edit file sudo vi /etc/ssl/openssl.cnf and add the following 

        [ v3_ca ]
        subjectAltName=IP:172.16.14.10

5. create self signed certificate. use the following script. You can fill anything for the field, except for "Common Name", you have to put the ip address of the VM where the registry is running, in this case 172.16.14.10

        cd registry
        openssl req -newkey rsa:4096 -nodes -sha256 -keyout ./certs/registry.key -x509 -days 365 -out ./certs/registry.crt

6. create docker-compose.yml

services:
        registry:
                image: registry:2
                ports:
                        - "5000:5000"
                volumes:
                        - ./certs:/certs
                        - ./data:/var/lib/registry
                environment:
                        REGISTRY_HTTP_TLS_CERTIFICATE : /certs/registry.crt
                        REGISTRY_HTTP_TLS_KEY : /certs/registry.key

7. Download and install docker-compose
        sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose

8. make directory /etc/docker/certs.d/172.16.14.10:5000/
9. copy file ~/certs/registry.crt into /etc/docker/certs.d/172.16.14.10:5000/ca.crt

        sudo mkdir -p /etc/docker/certs.d/172.16.14.10:5000/
        sudo cp certs/registry.crt /etc/docker/certs.d/172.16.14.10:5000/ca.crt

13. restart docker services 

        sudo systemctl restart docker

14. start registry container using 
        docker-compose up -d


# Copy registry certificate to all kubernetes nodes
8. copy registry certificate, in this case /home/registry/certs/registry.crt to all kubernetes nodes
9. on the kubernetes master, create the following directory /etc/docker/certs.d/172.16.14.10:5000
10. copy file registry.crt into directory /etc/docker/certs.d/172.16.14.10:5000
11. repeat step 8 and 9 on all kubernetes node

        #!/bin/bash
        for i in 172.16.11.1{0..3}
        do
            scp certs/registry.crt ${i}:~/
            ssh ${i} "sudo mkdir  -p /etc/docker/certs.d/172.16.14.10:5000; sudo cp ~/registry.crt /etc/docker/certs.d/172.16.14.10:5000/ca.crt"
            # ssh ${i} "sudo mkdir  -p /etc/container/certs.d/172.16.14.10:5000; sudo cp ~/registry.crt /etc/container/certs.d/172.16.14.10:5000/ca.crt"
        done



## on docker machine

1. create the container
2. tag the container
3. push the container into registry
