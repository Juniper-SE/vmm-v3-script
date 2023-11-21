#!/usr/bin/env python3
import apstra_api
# main program
ip_pools=['IP_POOLS1','IP_POOLS2','IP_POOLS3']
for i in ip_pools:
    print(f"delete ip pool {i}")
    apstra_api.delete_ip_pools(i)