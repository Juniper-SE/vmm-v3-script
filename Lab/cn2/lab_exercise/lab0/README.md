# Lab 0, Creating container image for the lab exercise
In this lab exercise, OCI compliant container image will created and uploaded into local private registry.

This container image will be used for the subsequent lab exercise.

## Steps

1. Upload  file [webserver.tgz](webserver.tgz) into node **registry**

        scp webserver.tgz registry:~/

2. open ssh session into node registry, and extract file webserver.tgz

        ssh registry
        tar xvpfz webserver.tgz 
3. The code is written using python with Flask Framework. You can modify the source code.

4. Create container image using podman

        cd webserver
        podman build -t 172.16.14.10:5000/webserver:0.1 .

5. Verify that container image has been created

        podman image ls

7. Push the container image into private registry (https://172.16.14.10:5000)

        podman push 172.16.14.10:5000/webserver:0.1
        
8. Verify that container image has been pushed into private registry

        curl -k https://172.16.14.10:5000/v2/_catalog
        curl -k https://172.16.14.10:5000/v2/webserver/tags/list