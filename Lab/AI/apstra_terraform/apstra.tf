terraform {
   required_providers {
     apstra = {
       source = "Juniper/apstra"
     }
   }
}
provider "apstra" {
    url = "https://172.16.10.2"
    tls_validation_disabled = true
    blueprint_mutex_enabled = false
    experimental = true
}


resource "apstra_logical_device" "ald1" {
  name = "AOS-10x1"
  panels = [
    {
      rows = 1
      columns = 10
      port_groups = [
        {
          port_count = 10
          port_speed = "1G"
          port_roles = ["superspine", "spine", "leaf", "peer", "access", "generic","unused"]
        },
      ]
    }
  ]
}


resource "apstra_asn_pool" "ASN_DC1_Spine" {
  name = "ASN_DC1_Spine"
  ranges = [
    {
      first = 4200001001
      last = 4200001010
    }
  ]
}
resource "apstra_asn_pool" "ASN_DC1_Leaf" {
  name = "ASN_DC1_Leaf"
  ranges = [
    {
      first = 4200001101
      last = 4200001110
    }
  ]
}
resource "apstra_asn_pool" "ASN_DC2" {
  name = "ASN_DC2"
  ranges = [
    {
      first = 4200002001
      last = 4200002010
    }
  ]
}


resource "apstra_ipv4_pool" "DC1_fabric_link" {
  name = "DC1_fabric_link"
  subnets = [
    { network = "10.1.0.0/24" }
  ]
}
resource "apstra_ipv4_pool" "DC1_Spine_loopback" {
  name = "DC1_Spine_loopback"
  subnets = [
    { network = "10.1.1.0/24" }
  ]
}
resource "apstra_ipv4_pool" "DC1_Leaf_loopback" {
  name = "DC1_Leaf_loopback"
  subnets = [
    { network = "10.1.2.0/24" }
  ]
}
resource "apstra_ipv4_pool" "DC1_VRF_loopback" {
  name = "DC1_VRF_loopback"
  subnets = [
    { network = "10.1.3.0/24" }
  ]
}
resource "apstra_ipv4_pool" "DC2_fabric_link" {
  name = "DC2_fabric_link"
  subnets = [
    { network = "10.2.0.0/24" }
  ]
}
resource "apstra_ipv4_pool" "DC2_Leaf_loopback" {
  name = "DC2_Leaf_loopback"
  subnets = [
    { network = "10.2.2.0/24" }
  ]
}
resource "apstra_ipv4_pool" "DC2_VRF_loopback" {
  name = "DC2_VRF_loopback"
  subnets = [
    { network = "10.2.3.0/24" }
  ]
}

resource "apstra_ipv6_pool" "DC1_fabric_link" {
  name = "DC1_fabric_link"
  subnets = [
    { network = "fc00:dead:beef:1000::/64" }
  ]
}
resource "apstra_ipv6_pool" "DC1_Spine_loopback" {
  name = "DC1_Spine_loopback"
  subnets = [
    { network = "fc00:dead:beef:1001::/64" }
  ]
}
resource "apstra_ipv6_pool" "DC1_Leaf_loopback" {
  name = "DC1_Leaf_loopback"
  subnets = [
    { network = "fc00:dead:beef:1002::/64" }
  ]
}
resource "apstra_ipv6_pool" "DC1_VRF_loopback" {
  name = "DC1_VRF_loopback"
  subnets = [
    { network = "fc00:dead:beef:1003::/64" }
  ]
}
resource "apstra_ipv6_pool" "DC2_fabric_link" {
  name = "DC2_fabric_link"
  subnets = [
    { network = "fc00:dead:beef:2000::/64" }
  ]
}
resource "apstra_ipv6_pool" "DC2_Leaf_loopback" {
  name = "DC2_Leaf_loopback"
  subnets = [
    { network = "fc00:dead:beef:2002::/64" }
  ]
}
resource "apstra_ipv6_pool" "DC2_VRF_loopback" {
  name = "DC2_VRF_loopback"
  subnets = [
    { network = "fc00:dead:beef:2003::/64" }
  ]
}

resource "apstra_configlet" "user_admin" {
  name = "user_admin"
  generators = [
    {
      config_style  = "junos"
      section       = "top_level_hierarchical"
      template_text = <<-EOT
				system {
				    root-authentication {
				        encrypted-password "$1$Jw5Ubokd$OLC5bOaYt.cI5fg0vz6F4."; ## SECRET-DATA
				    }
				    login {
				        user admin {
				            class super-user;
				            authentication {
				                encrypted-password "$1$Jw5Ubokd$OLC5bOaYt.cI5fg0vz6F4."; ## SECRET-DATA
				                ssh-rsa "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDBUA+4YJwqE2rqwweZ3NG7GpXF3JqIxFbnDxraW8//QWjHLGVgn+jFbXFB3T/yLYpIRAh8SsAw6M6pZXzGd3oiltENLkoN5YGI1yW0bCTsS/Z4BoW/iuPR2rYQqhA+NPi9OZO/opVbJ+VIdfm+fugWPSVpduBiJN20P9iEF1zCW4EmWZn3qkl25LjVSBVMiwn+crcsCHUub3xDRicgTOOINFo4lZy03Fsa3PoqpxXv18FhNi3pVWmV2n3vIckWt8BbaPWMTFZmERHkVb4Y15GsHwcQxb6gm3h8Do4QgURbujCUJQhpJT4BRdD8kja1NQK4lbcPq6l9rF3YM7aQkscB16nCplWcgdnxI7eN//FA4ovvx7d57i43Y7GzSlQE87kcIDDQ1eCesYOfg9EfqCFSVWV0hbhc2Ap6YCoc0R9POpG1n0LO+o++h0J0bkLUWsIiQLb3LiC91FnP3giK5MEzdJ+maJcjIyGlTth52s01nLdT4gQDgTURqIpfL8L0HWE= irzan@irzan-mbp"; ## SECRET-DATA
				            }
				        }
				    }
				}
      EOT
    }
  ]
}