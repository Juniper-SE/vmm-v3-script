cat << EOF | tee command_servers.yml 
---        
command_servers:
    server1:
        ip: 172.16.11.101
        connection: ssh
        ssh_user: ubuntu
        ssh_pass: pass01
        sudo_pass: pass01
        ntpserver: ntp.juniper.net

        registry_insecure: false
        container_registry: hub.juniper.net/contrail
        container_tag: ${CONTAINER_TAG}
        container_registry_username: ${REGISTRY_USER}
        container_registry_password: ${REGISTRY_PASSWORD}
        config_dir: /etc/contrail

        contrail_config:
            database:
                type: postgres
                dialect: postgres
                password: contrail123
            keystone:
                assignment:
                    data:
                        users:
                            admin:
                                password: pass01
            insecure: true
            client:
                password: pass01
EOF