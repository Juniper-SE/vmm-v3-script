#!/usr/bin/env python3
mask_ipv4 = 0b1
mask_ipv6 = 0b10
mask_iso  = 0b100
mask_mpls = 0b1000
mask_isis = 0b10000
mask_rsvp = 0b100000
mask_ldp  = 0b1000000
mask_rpm  = 0b10000000
mask_mtu  = 0b100000000
mask = mask_ipv4 |  mask_iso | mask_mpls | mask_isis | mask_rsvp | mask_ldp | mask_mtu
# mask = mask_ipv4 |  mask_iso |  mask_isis
print(f"mask value {hex(mask)} {bin(mask)}")
