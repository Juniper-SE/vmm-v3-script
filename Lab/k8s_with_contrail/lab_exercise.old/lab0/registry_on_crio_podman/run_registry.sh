podman run --name registry \
	-p 5000:5000 \
	-v ./data:/var/lib/registry \
	-v ./certs:/certs \
	-e "REGISTRY_HTTP_TLS_CERTIFICATE=/certs/registry.crt" \
	-e "REGISTRY_HTTP_TLS_KEY=/certs/registry.key" \
	-d registry:2 
