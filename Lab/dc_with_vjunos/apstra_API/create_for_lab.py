#!/usr/bin/env python3
import apstra_api
import yaml

# Create ASN Pools
asn="""
items:
- name: ASN_DC1_Spine
  first: 4200001001
  last: 4200001010
- name: ASN_DC1_Leaf
  first: 4200001101
  last: 4200001110
- name: ASN_DC2
  first: 4200002001
  last: 4200002010
"""

asn_dict = yaml.load(asn,Loader=yaml.FullLoader)
for i in asn_dict['items']:
    print(f"creating pool {i['name']}")
    apstra_api.create_asn_pools(i)

# Create IP pools

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
"""
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"creating ip pool {i['name']}")
    apstra_api.create_ip_pools(i)

# create IPv6 Pools
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
"""
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"creating ip pool {i['name']}")
    apstra_api.create_ipv6_pools(i)


# create Logical devices
ld="""
items:
  - display_name: AOS_12x1
    id : AOS_12x1
    panels:
    - panel_layout:
        column_count: 12
        row_count: 1
      port_groups:
      - count: 12
        roles:
        - generic
        - superspine
        - access
        - leaf
        - spine
        - peer
        speed:
          unit: G
          value: 1
      port_indexing:
        order: T-B, L-R
        schema: absolute
        start_index: 1

"""

ld_dict = yaml.load(ld,Loader=yaml.FullLoader)
for i in ld_dict['items']:
  apstra_api.create_logical_devices(i)
