#!/usr/bin/env python3
import apstra_api
import yaml
# main program

# ippools="""
# items:
# - name: IPv6_POOLS1
#   subnets:
#   - network: fc00:dead:beef:1001::/64
#   - network: fc00:dead:beef:1002::/64
#   - network: fc00:dead:beef:1003::/64
# - name: IPv6_POOLS2
#   subnets:
#   - network: fc00:dead:beef:2001::/64
#   - network: fc00:dead:beef:2002::/64
#   - network: fc00:dead:beef:2003::/64
# - name: IPv6_POOLS3
#   subnets:
#   - network: fc00:dead:beef:3001::/64
#   - network: fc00:dead:beef:3002::/64
#   - network: fc00:dead:beef:3003::/64
# """

ippools="""
items:
- name: DC1_fabric_link
  subnets:
  - network: fc00:dead:beef:1000::/64
- name: DC1_Spine_loopback
  subnets:
  - network: fc00:dead:beef:1001::/64
- name: DC1_Leaf_loopback
  subnets:
  - network: fc00:dead:beef:1002::/64
- name: DC1_VRF_loopback
  subnets:
  - network: fc00:dead:beef:1003::/64
- name: DC2_fabric_link
  subnets:
  - network: fc00:dead:beef:2000::/64
- name: DC2_Leaf_loopback
  subnets:
  - network: fc00:dead:beef:2002::/64
- name: DC2_VRF_loopback
  subnets:
  - network: fc00:dead:beef:2003::/64
- name: DC3_fabric_link
  subnets:
  - network: fc00:dead:beef:3000::/64
- name: DC3_Spine_loopback
  subnets:
  - network: fc00:dead:beef:3001::/64
- name: DC3_Leaf_loopback
  subnets:
  - network: fc00:dead:beef:3002::/64
- name: DC3_VRF_loopback
  subnets:
  - network: fc00:dead:beef:3003::/64
"""
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"creating ip pool {i['name']}")
    apstra_api.create_ipv6_pools(i)