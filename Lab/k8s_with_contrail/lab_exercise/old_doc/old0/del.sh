curl -X PUT -H "Content-Type: application/json; charset=UTF-8" \
-d '{ "virtual-network": \
		  { \
				"fq_name" :["default-domain","k8s-ns-user-1","k8s-vn-external-pod-network"], 
				"router_external":False, \
			} 
		}' \
		http://172.16.11.10:8082/virtual-network/7bc27d1a-255f-4e19-9ac1-66ec32bb3ddb 
