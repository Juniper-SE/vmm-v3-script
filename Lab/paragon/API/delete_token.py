#!/usr/bin/env python3
import requests
import json
import sys
if len(sys.argv) > 1:
    token = sys.argv[1]
    url=f"https://172.16.12.1/api/v1/self/apitokens/{token}"
    print(url)
    email="irzan@juniper.net"
    password="J4k4rt4#170845"
    # data={
    #     'email': email,
    #     'password': password
    # }
    #headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
    r=requests.delete(url,verify=False,auth=('irzan@juniper.net','J4k4rt4#170845'))
    print(f"status {r.status_code}")
    print(f"headers {r.headers}")
    print(f"result {r.text}")
else:
    print("where is the token ID  ?")
