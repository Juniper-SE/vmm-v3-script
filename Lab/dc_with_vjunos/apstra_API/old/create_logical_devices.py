#!/usr/bin/env python3
import apstra_api
import yaml
# main program
# ld="""
# items:
#   - display_name: vEX_Leaf
#     panels:
#     - panel_layout:
#         column_count: 10
#         row_count: 1
#       port_groups:
#       - count: 2
#         roles:
#         - spine
#         speed:
#           unit: G
#           value: 1
#       - count: 8
#         roles:
#         - generic
#         - access
#         speed:
#           unit: G
#           value: 1
#       port_indexing:
#         order: T-B, L-R
#         schema: absolute
#         start_index: 1
#   - display_name: vEX_Spine
#     panels:
#     - panel_layout:
#         column_count: 10
#         row_count: 1
#       port_groups:
#       - count: 10
#         roles:
#         - superspine
#         - generic
#         - leaf
#         speed:
#           unit: G
#           value: 1
#       port_indexing:
#         order: T-B, L-R
#         schema: absolute
#         start_index: 1
#   - display_name: vEX_Collapsed
#     panels:
#     - panel_layout:
#         column_count: 10
#         row_count: 1
#       port_groups:
#       - count: 10
#         roles:
#         - superspine
#         - generic
#         - leaf
#         - access
#         - spine
#         speed:
#           unit: G
#           value: 1
#       port_indexing:
#         order: T-B, L-R
#         schema: absolute
#         start_index: 1
# """

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
