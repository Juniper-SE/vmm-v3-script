cat << EOF | sudo tee /containers_data/tftp/custom_config/junos_custom1.sh
#!/bin/sh
cli -c "configure; set system commit synchronize; set chassis evpn-vxlan-default-switch-support; commit and-quit"
EOF
sudo chmod +x /containers_data/tftp/custom_config/junos_custom1.sh