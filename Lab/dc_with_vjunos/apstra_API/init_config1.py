#!/usr/bin/env python3
import apstra_api
import yaml
# main program

# asn="""
# items:
# - name: ASN_Spine_DC1
#   first: 4200001001 
#   last: 4200001009
# - name: ASN_Leaf_DC1
#   first: 4200001011
#   last: 4200001019
# - name: ASN_Collapsed_DC2
#   first: 4200002011
#   last: 4200002019
# - name: ASN_Spine_DC3
#   first: 4200003001 
#   last: 4200003009
# - name: ASN_Leaf_DC3
#   first: 4200003011
#   last: 4200003019
# """
asn="""
items:
- name: ASN_Spine_DC1
  first: 4200001001 
  last: 4200001009
- name: ASN_Leaf_DC1
  first: 4200001011
  last: 4200001019
"""
asn_dict = yaml.load(asn,Loader=yaml.FullLoader)
for i in asn_dict['items']:
    print(f"creating pool {i['name']}")
    apstra_api.create_asn_pools(i)

# ippools="""
# items:
# - name: Fabric_link_DC1
#   subnets:
#   - network: 10.101.0.0/24
# - name: Loopback_Spine_DC1
#   subnets:
#   - network: 10.101.1.0/24
# - name: Loopback_Leaf_DC1
#   subnets:
#   - network: 10.101.2.0/24
# - name: Loopback_VRF_DC1
#   subnets:
#   - network: 10.101.3.0/24
# - name: Fabric_link_DC2
#   subnets:
#   - network: 10.102.0.0/24
# - name: Loopback_Collapsed_DC2
#   subnets:
#   - network: 10.102.2.0/24
# - name: Loopback_VRF_DC2
#   subnets:
#   - network: 10.102.3.0/24
# - name: Fabric_link_DC3
#   subnets:
#   - network: 10.103.0.0/24
# - name: Loopback_Spine_DC3
#   subnets:
#   - network: 10.103.1.0/24
# - name: Loopback_Leaf_DC3
#   subnets:
#   - network: 10.103.2.0/24
# - name: Loopback_VRF_DC3
#   subnets:
#   - network: 10.103.3.0/24
# """
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
"""
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"creating ip pool {i['name']}")
    apstra_api.create_ip_pools(i)


# ippools="""
# items:
# - name: Loopback_Spine_DC1
#   subnets:
#   - network: fc00:dead:beef:1011::/64
# - name: Loopback_Leaf_DC1
#   subnets:
#   - network: fc00:dead:beef:1012::/64
# - name: Loopback_VRF_DC1
#   subnets:
#   - network: fc00:dead:beef:1013::/64
# - name: Loopback_Collapsed_DC2
#   subnets:
#   - network: fc00:dead:beef:2012::/64
# - name: Loopback_VRF_DC2
#   subnets:
#   - network: fc00:dead:beef:2013::/64
# - name: Loopback_Spine_DC3
#   subnets:
#   - network: fc00:dead:beef:3011::/64
# - name: Loopback_Leaf_DC3
#   subnets:
#   - network: fc00:dead:beef:3012::/64
# - name: Loopback_VRF_DC3
#   subnets:
#   - network: fc00:dead:beef:3013::/64
# """
ippools="""
items:
- name: Loopback_Spine_DC1
  subnets:
  - network: fc00:dead:beef:1011::/64
- name: Loopback_Leaf_DC1
  subnets:
  - network: fc00:dead:beef:1012::/64
- name: Loopback_VRF_DC1
  subnets:
  - network: fc00:dead:beef:1013::/64
"""
ippools_dict = yaml.load(ippools,Loader=yaml.FullLoader)
for i in ippools_dict['items']:
    print(f"creating ip pool {i['name']}")
    apstra_api.create_ipv6_pools(i)

# ld="""
# items:
# - display_name: vEX_Spine
#   panels:
#   - panel_layout:
#       column_count: 10
#       row_count: 1
#     port_groups:
#     - count: 10
#       roles:
#       - superspine
#       - unused
#       - leaf
#       - generic
#       speed:
#         unit: G
#         value: 1
#     port_indexing:
#       order: T-B, L-R
#       schema: absolute
#       start_index: 1
# - display_name: vEX_Leaf
#   panels:
#   - panel_layout:
#       column_count: 10
#       row_count: 1
#     port_groups:
#     - count: 2
#       roles:
#       - spine
#       speed:
#         unit: G
#         value: 1
#     - count: 8
#       roles:
#       - unused
#       - generic
#       - access
#       speed:
#         unit: G
#         value: 1
#     port_indexing:
#       order: T-B, L-R
#       schema: absolute
#       start_index: 1
# - display_name: vEX_Collapsed
#   panels:
#   - panel_layout:
#       column_count: 10
#       row_count: 1
#     port_groups:
#     - count: 10
#       roles:
#       - superspine
#       - unused
#       - leaf
#       - generic
#       - peer
#       - access
#       - spine
#       speed:
#         unit: G
#         value: 1
#     port_indexing:
#       order: T-B, L-R
#       schema: absolute
#       start_index: 1
# """
# - display_name: vEVO_Spine
#   panels:
#   - panel_layout:
#       column_count: 12
#       row_count: 1
#     port_groups:
#     - count: 12
#       roles:
#       - superspine
#       - leaf
#       - generic
#       speed:
#         unit: G
#         value: 10
#     port_indexing:
#       order: T-B, L-R
#       schema: absolute
#       start_index: 1
# """

# ld_dict = yaml.load(ld,Loader=yaml.FullLoader)
# for i in ld_dict['items']:
#   apstra_api.create_logical_devices(i)
