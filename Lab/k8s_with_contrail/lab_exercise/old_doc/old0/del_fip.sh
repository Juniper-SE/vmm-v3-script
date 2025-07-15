# URL1=http://172.16.11.10:8082/ref-update
# URL1=http://172.16.11.10:8082/virtual-network/b40af355-b3ba-4966-83e6-c829dffa4ae7
# HEADER="Content-Type: application/json; charset=UTF-8"
# DATA='{ "operation" : "DELETE", "uuid" : "e546bb40-958e-4323-bd6c-01b75348cf46", "type":"floating-ip-pool","ref-type":"virtual-network","ref-uuid":"b40af355-b3ba-4966-83e6-c829dffa4ae7" }'
# DATA='{ "virtual-network" : {"floating_ip_pools" : []}}'
# curl -X PUT -H "$HEADER" -d '$DATA' $URL1
#curl -X PUT -H "Content-Type: application/json; charset=UTF-8" -d '{ "virtual-network" : {"fq_name": [ "default-domain", "k8s-ns-user-1", "k8s-vn-external-pod-network" ],"floating_ip_pools": "" }}' http://172.16.11.10:8082/virtual-network/b40af355-b3ba-4966-83e6-c829dffa4ae7
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"operation": "DELETE", ref-uuid: "c0efe9a3-73fe-405e-8a20-2ec4491372ad", "type":"virtual-network", "ref-type": "floating-ip-pool","ref":"73701896-ed06-4d15-8d50-910ad209b3fc"}' http://172.16.11.10:8082/ref-update
