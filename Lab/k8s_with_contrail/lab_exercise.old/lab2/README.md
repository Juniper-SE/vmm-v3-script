# Lab 2

## create namespace, ns1 as non-isolated namespace and ns2 as isolated namespace

        kubectl apply -f lab2_ns_non_isolated.yaml
        curl http://<contrail_controller>:8082/virtual-networks

        kubectl apply -f lab2_ns_isolated.yaml
        curl http://<contrail_controller>:8082/virtual-networks

k8s manifest: [lab2_ns_non_isolated.yaml](lab2_ns_non_isolated.yaml)

k8s manifest: [lab2_ns_isolated.yaml](lab2_ns_isolated.yaml)

## start pods and deployment in the namespaces

to start the pods and deployment

        kubectl apply -f lab2_client_ns1.yaml
        kubectl apply -f lab2_client_ns2.yaml
        kubectl apply -f lab2_lb_ns1.yaml
        kubectl apply -f lab2_lb_ns2.yaml

to verify the pods

        kubectl get pods --all-namespaces -o wide
        kubectl get services --all-namespaces -o wide

k8s manifest: [lab2_client_ns1.yaml](lab2_client_ns1.yaml)

k8s manifest: [lab2_client_ns2.yaml](lab2_client_ns2.yaml)

k8s manifest: [lab2_lb_ns1.yaml](lab2_lb_ns1.yaml)

k8s manifest: [lab2_lb_ns2.yaml](lab2_lb_ns2.yaml)

## test connectivity between different pods on different namespaces

        kubectl exec -it <pod_name> -n <name_space> -- sh 
        
## create another floating ip pools and assign it to the object

create floating ip pools

        kubectl apply -f vn_public2.yaml
        ../config_lab.py set_rt -c vn_public2_rt_fip.yaml

k8s manifest: [vn_public2.yaml](vn_public2.yaml)
Route target and FIP : [vn_public2_rt_fip.yaml](vn_public2_rt_fip.yaml)

create deployment with floating ip 

        kubectl apply -f lab2_lb7_default.yaml
        kubectl get services

k8s manifest: [lab2_lb7_default.yaml](lab2_lb7_default.yaml)

## create namespace with virtual network for floating ip 

create namespace and virtual network 

        kubectl apply -f lab2_ns_ns3.yaml

k8s manifest: [lab2_ns_ns3.yaml](lab2_ns_ns3.yaml)

create deployment in namespace NS3

        kubectl apply -f lab2_lb8_ns3.yaml
        kubectl get svc -n ns3
    
k8s manifest: [lab2_lb8_ns3.yaml](lab2_lb8_ns3.yaml)


create deployment in namespace ns3 but with floating ip from global

        kubectl apply -f lab2_lb9_ns3.yaml
        kubectl get svc -n ns3

k8s manifest: [lab2_lb9_ns3.yaml](lab2_lb9_ns3.yaml)

