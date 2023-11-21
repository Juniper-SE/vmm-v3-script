# Lab 1

##  create pods

To create pod

        kubectl apply -f lab1_client.yaml

k8s manifest : [lab1_client.yaml](lab1_client.yaml)

to verify 

        kubectl get pods -o wide
        kubectl exec -it <pod_name> -- sh

## create pod with multiple container

To create pod with multiple containers. Note it will fail because both container are running service on the same TCP port 

        kubectl apply -f lab1_pod0.yaml
        kubectl get pods 
        kubectl describe pod <pod_name>

k8s manifest: [lab1_pod0.yaml](lab1_pod0.yaml)

Run another pod with multile containers, but the 2nd container is configured to run a modified script to run the services on different TCP Port.

        upload the script to the nfs server, and modify the port number from 80 to 8080

        kubectl apply -f lab1_pod1.yaml
        kubectl get pods
        kubectl des ribe pod <pod_name>

k8s manifest: [lab1_pod1.yaml](lab1_pod1.yaml)

script running on container : [webserver.py](../container/webserver/webserver.py). Edit it, to modify port 80 to 8080 (line 72)


##  create deployment and nodeport

To create deployment and nodeport

        kubectl apply -f lab1_nodeport.yaml
        kubectl get pods -o wide
        kubectl get services

to verify, from node **gw** initial curl request to the worker's node ip address and the port specified on the services

        curl http://<worker_node_ip>:<port>

k8s manifest: [lab1_nodeport.yaml](lab1_nodeport.yaml)

## configure bgp peer to the SDN Gateway on contrail controller

To configure BGP peer the SDN gateway 

        curl http://<contrail_controller>:8082/bgp-routers | python3 -m json.tool
        sdngw_config/create_bgp_router.py
        curl http://<contrail_controller>:8082/bgp-routers | python3 -m json.tool

the script to configure BGP peer on contrail [sdngw_config/create_bgp_router.py](sdngw_config/create_bgp_router.py)
        
configuration of SDN gateway : [sdngw.conf](sdngw_config/sdngw.conf)

configuration of FRR running on node **GW** : [bgpd.conf](sdngw_config/bgpd.conf)

## create virtual network 

        kubectl apply -f vn-public.yaml
        curl http://<contrail_controller>:8082/virtual-networks | python3 -m json.tool

k8s manifest : [vn-public.yaml](vn-public.yaml)

## on contrail, configure route target (export/import) and floating ip pools

        ../config_lab.py set_rt -c lab1_contrail.yaml
        curl http://<contrail_controller>:8082/virtual-networks | python3 -m json.tool

script to configure route target (export and import) and floating ip pools on contrail : [config_lab.py](../config_lab.py)

configuration file for the script : [lab1_contrail.yaml](lab1_contrail.yaml)

## create deployment and load balancer

to create deployment and load balancer 

        kubectl apply -f lab1_lb.yaml
        kubectl get pods
        kubectl get services

k8s manifest to create deployment and load balancer : [lab1_lb.yaml](lab1_lb.yaml)

## create deployment and ingress

to create deployment and ingress

        kubectl apply -f lab1_ingress.yaml
        kubectl get pods
        kubectl get services
        kubectl get ingress

k8s manifest to create deployment and load balancer : [lab1_ingress.yaml](lab1_ingress.yaml)
        




