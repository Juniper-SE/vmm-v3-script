variable "logical_device_name" {
    type = string
    default = "AOS-20x1"
}

data "apstra_logical_device" "selected1" {
    name = var.logical_device_name
}
output "ld_id" {
    value = data.apstra_logical_device.selected1.id
}
