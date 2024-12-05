data "apstra_logical_device" "selected" {
  name = "AOS-10x1"
}

variable "device_profile" {
    default = "29df9a23-5815-4d71-8d85-25e3db30b069"
}

resource "apstra_interface_map" "aim" {
  name              = "vjunos"
  logical_device_id = data.apstra_logical_device.selected.id
  device_profile_id = var.device_profile
  interfaces = [
    {
      "logical_device_port"     = "1/1"
      "physical_interface_name" = "ge-0/0/0"
      "transformation_id"       = 1
    },
    {
      "logical_device_port"     = "1/2"
      "physical_interface_name" = "ge-0/0/1"
    },
    {
      "logical_device_port"     = "1/3"
      "physical_interface_name" = "ge-0/0/2"
    },
    {
      "logical_device_port"     = "1/4"
      "physical_interface_name" = "ge-0/0/3"
    },
    {
      "logical_device_port"     = "1/5"
      "physical_interface_name" = "ge-0/0/4"
    },
    {
      "logical_device_port"     = "1/6"
      "physical_interface_name" = "ge-0/0/5"
    },
    {
      "logical_device_port"     = "1/7"
      "physical_interface_name" = "ge-0/0/6"
    },
    {
      "logical_device_port"     = "1/8"
      "physical_interface_name" = "ge-0/0/7"
    },
    {
      "logical_device_port"     = "1/9"
      "physical_interface_name" = "ge-0/0/8"
    },
    {
      "logical_device_port"     = "1/10"
      "physical_interface_name" = "ge-0/0/9"
    }
  ]
}

resource "apstra_rack_type" "rack_type_1" {
  name                       = "rack_type_1"
  description                = "rack_type_1"
  fabric_connectivity_design = "l3clos"
  leaf_switches = { // leaf switches are a map keyed by switch name, so
    leaf_switch = { // "leaf switch" on this line is the name used by links targeting this switch.
      logical_device_id   = data.apstra_logical_device.selected.id
      spine_link_count    = 1
      spine_link_speed    = "1G"
      redundancy_protocol = "esi"
    }
  }
}
resource "apstra_rack_type" "rack_type2" {
  name                       = "rack_type_2"
  description                = "rack_type_2"
  fabric_connectivity_design = "l3collapsed"
  leaf_switches = { // leaf switches are a map keyed by switch name, so
    leaf_switch = { // "leaf switch" on this line is the name used by links targeting this switch.
      logical_device_id   = data.apstra_logical_device.selected.id
      redundancy_protocol = "esi"
    }
  }
}