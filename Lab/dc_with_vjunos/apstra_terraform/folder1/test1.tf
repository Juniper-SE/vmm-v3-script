resource "apstra_logical_device" "ald2" {
  name = "AOS-20x1"
  panels = [
    {
      rows = 1
      columns = 20
      port_groups = [
        {
          port_count = 20
          port_speed = "1G"
          port_roles = ["superspine", "spine", "leaf", "peer", "access", "generic","unused"]
        },
      ]
    }
  ]
}