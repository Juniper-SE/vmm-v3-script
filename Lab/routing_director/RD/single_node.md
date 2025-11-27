# Single node installation

## requirement

    RAM: 64G
    vCPU: 32
    HD: 400G

## configuration for single node deployment

    # installation for single node VM (lab only)
    #
    # for single node installation (strictly for demo, not production) add the following
    # set paragon cluster install scale-mode single

    configure
    set deployment cluster nodes kubernetes 1 address 172.16.11.11
    set deployment cluster install scale-mode single
    set deployment cluster ntp ntp-servers ntp.juniper.net
    set deployment cluster common-services ingress ingress-vip 172.16.12.1
    set deployment cluster applications active-assurance test-agent-gateway-vip 172.16.12.2
    set deployment cluster applications web-ui web-admin-user "irzan@juniper.net"   
    set deployment cluster applications web-ui web-admin-password "J4k4rt4#170845" 
    set deployment cluster applications pathfinder pce-server pce-server-vip 172.16.12.3
    set deployment cluster install enable-l3-vip true
    set deployment cluster common-services metallb metallb-bgp-peer peer-ip 172.16.11.254 peer-asn 65100 local-asn 65101 local-nodes 172.16.11.11 
    commit
    exit