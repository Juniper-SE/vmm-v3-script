#!/usr/bin/env python3
import apstra_api
import yaml
# main program

asn="""
items:
- name: ASN_DC1_Spine
  first: 65001
  last: 65009
- name: ASN_DC1_Leaf
  first: 65011
  last: 65019
- name: ASN_DC2_Collapsed
  first: 65021
  last: 65029
- name: ASN_DC3_Spine
  first: 65031
  last: 65039
- name: ASN_DC3_Leaf
  first: 65041
  last: 65049
"""
asn_dict = yaml.load(asn,Loader=yaml.FullLoader)
for i in asn_dict['items']:
    print(f"deleting pool {i['name']}")
    apstra_api.delete_asn_pools(i['name'])

ippools="""
items:
- name: Fabric_link_DC1
  subnets:
  - network: 10.101.0.0/24
- name: Loopback_Spine_DC1
  subnets:
  - network: 10.101.1.0/24
- name: Loopback_Leaf_DC1
  subnets:
  - network: 10.101.2.0/24
- name: Loopback_VRF_DC1
  subnets:
  - network: 10.101.3.0/24
- name: Fabric_link_DC2
  subnets:
  - network: 10.102.0.0/24
- name: Loopback_Collapsed_DC1
  subnets:
  - network: 10.102.2.0/24
- name: Loopback_VRF_DC2
  subnets:
  - network: 10.102.3.0/24
- name: Fabric_link_DC3
  subnets:
  - network: 10.103.0.0/24
- name: Loopback_Spine_DC3
  subnets:
  - network: 10.103.1.0/24
- name: Loopback_Leaf_DC3
  subnets:
  - network: 10.103.2.0/24
- name: Loopback_VRF_DC3
  subnets:
  - network: 10.103.3.0/24
"""
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"deleting ip pool {i['name']}")
    apstra_api.delete_ip_pools(i['name'])


ippools="""
items:
- name: Fabric_link_DC1
  subnets:
  - network: fc00:dead:beef:100::/64
- name: Loopback_Spine_DC1
  subnets:
  - network: fc00:dead:beef:101::/64
- name: Loopback_Leaf_DC1
  subnets:
  - network: fc00:dead:beef:102::/64
- name: Loopback_VRF_DC1
  subnets:
  - network: fc00:dead:beef:103::/64
- name: Fabric_link_DC2
  subnets:
  - network: fc00:dead:beef:200::/64
- name: Loopback_Collapsed_DC1
  subnets:
  - network: fc00:dead:beef:202::/64
- name: Loopback_VRF_DC2
  subnets:
  - network: fc00:dead:beef:203::/64
- name: Fabric_link_DC3
  subnets:
  - network: fc00:dead:beef:300::/64
- name: Loopback_Spine_DC3
  subnets:
  - network: fc00:dead:beef:301::/64
- name: Loopback_Leaf_DC3
  subnets:
  - network: fc00:dead:beef:302::/64
- name: Loopback_VRF_DC3
  subnets:
  - network: fc00:dead:beef:303::/64
"""
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"creating ip pool {i['name']}")
    apstra_api.delete_ipv6_pools(i['name'])

ld="""
items:
  - display_name: vEX_Leaf
    panels:
    - panel_layout:
        column_count: 10
        row_count: 1
      port_groups:
      - count: 2
        roles:
        - spine
        speed:
          unit: G
          value: 1
      - count: 8
        roles:
        - generic
        - access
        speed:
          unit: G
          value: 1
      port_indexing:
        order: T-B, L-R
        schema: absolute
        start_index: 1
  - display_name: vEX_Spine
    panels:
    - panel_layout:
        column_count: 10
        row_count: 1
      port_groups:
      - count: 10
        roles:
        - superspine
        - generic
        - leaf
        speed:
          unit: G
          value: 1
      port_indexing:
        order: T-B, L-R
        schema: absolute
        start_index: 1
  - display_name: vEX_Collapsed
    panels:
    - panel_layout:
        column_count: 10
        row_count: 1
      port_groups:
      - count: 10
        roles:
        - superspine
        - generic
        - leaf
        - access
        - spine
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
  print(f"deleting {i['display_name']}")
  apstra_api.delete_logical_devices(i['display_name'])