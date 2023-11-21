#!/usr/bin/env python3
import apstra_api
# main program
ip_pools=['IPv6_POOLS1','IPv6_POOLS2','IPv6_POOLS3']
for i in ip_pools:
    print(f"delete ip pool {i}")
    apstra_api.delete_ipv6_pools(i)