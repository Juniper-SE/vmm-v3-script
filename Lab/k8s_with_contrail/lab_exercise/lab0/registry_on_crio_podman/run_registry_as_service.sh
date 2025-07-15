podman generate systemd --new --name registry | sudo tee /etc/systemd/system/registry.service
sudo systemctl enable registry
podman stop registry
podman rm registry
sudo systemctl start registry