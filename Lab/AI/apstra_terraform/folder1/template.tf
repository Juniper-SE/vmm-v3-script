locals {
  rack_name_and_count = {
    "tduowjdmr3-gm2t4vmpgjw" = 3
  }
}

data "apstra_logical_device" "s1" {
  name = "AOS-10x1"
}

# Instantiate a template using the Rack Type IDs
# and counts defined above.
resource "apstra_template_rack_based" "dc1" {
  name                     = "dc1"
  asn_allocation_scheme    = "unique"
  overlay_control_protocol = "evpn"
  spine = {
    logical_device_id = data.apstra_logical_device.s1.id
    count             = 2
  }
  rack_infos = {
    for name, count in local.rack_name_and_count : name => { count = count }
  }
}