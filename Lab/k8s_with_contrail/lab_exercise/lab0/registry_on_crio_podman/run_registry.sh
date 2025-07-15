podman run --name registry \
	-p 5000:5000 \
	-v ~/registry/data:/var/lib/registry \
	-v ~/registry/certs:/certs \
	-e "REGISTRY_HTTP_TLS_CERTIFICATE=/certs/registry.crt" \
	-e "REGISTRY_HTTP_TLS_KEY=/certs/registry.key" \
        --restart=always \
        --network podman \
	-d registry:2 
