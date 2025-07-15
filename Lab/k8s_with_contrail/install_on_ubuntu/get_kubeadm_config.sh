kubectl -n kube-system get configmap kubeadm-config -o jsonpath='{.data.ClusterConfiguration}' > kubeadm.yaml
echo "  certSANs:" >> kubeadm.yaml
echo '    - "127.0.0.1"' >> kubeadm.yaml
echo '    - "172.16.11.10"' >> kubeadm.yaml
echo '    - "10.96.0.1"' >> kubeadm.yaml


