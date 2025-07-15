#!/usr/bin/env python3
import apstra_api
import yaml
# main program

# ippools="""
# items:
# - name: IP_POOLS1
#   subnets:
#   - network: 10.1.1.0/24
#   - network: 10.1.2.0/24
#   - network: 10.1.3.0/24
# - name: IP_POOLS2
#   subnets:
#   - network: 10.2.1.0/24
#   - network: 10.2.2.0/24
#   - network: 10.2.3.0/24
# - name: IP_POOLS3
#   subnets:
#   - network: 10.3.1.0/24
#   - network: 10.3.2.0/24
#   - network: 10.3.3.0/24
# """

ippools="""
items:
- name: DC1_fabric_link
  subnets:
  - network: 10.1.0.0/24
- name: DC1_Spine_loopback
  subnets:
  - network: 10.1.1.0/24
- name: DC1_Leaf_loopback
  subnets:
  - network: 10.1.2.0/24
- name: DC1_VRF_loopback
  subnets:
  - network: 10.1.3.0/24
- name: DC2_fabric_link
  subnets:
  - network: 10.2.0.0/24
- name: DC2_Leaf_loopback
  subnets:
  - network: 10.2.2.0/24
- name: DC2_VRF_loopback
  subnets:
  - network: 10.2.3.0/24
- name: DC3_fabric_link
  subnets:
  - network: 10.3.0.0/24
- name: DC3_Spine_loopback
  subnets:
  - network: 10.3.1.0/24
- name: DC3_Leaf_loopback
  subnets:
  - network: 10.3.2.0/24
- name: DC3_VRF_loopback
  subnets:
  - network: 10.3.3.0/24
"""
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"creating ip pool {i['name']}")
    apstra_api.create_ip_pools(i)