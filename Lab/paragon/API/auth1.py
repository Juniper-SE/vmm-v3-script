#!/usr/bin/env python3
import requests
import json
url="https://172.16.12.1/api/v1/login"
email="irzan@juniper.net"
password="J4k4rt4#170845"
data={
    'email': email,
    'password': password
}
headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
r=requests.post(url,verify=False,data=data)
print(f"status {r.status_code}")
print(f"headers {r.headers}")
csrtoken=r.headers['Set-Cookie'].split(':')[0].split(';')[0].split('=')[1]
print(f"csrtoken {csrtoken}")