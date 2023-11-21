kubectl -n kube-system get configmap kubeadm-config -o jsonpath='{.data.ClusterConfiguration}' > kubeadm.yaml
sed -i -e '1a certSANs:' kubeadm.yaml
sed -i -e '2s/^/  /' kubeadm.yaml
sed -i -e '2a - 127.0.0.1' kubeadm.yaml
sed -i -e '3s/^/    /' kubeadm.yaml
sed -i -e '3a - 172.16.11.10' kubeadm.yaml
sed -i -e '4s/^/    /' kubeadm.yaml
sed -i -e '4a - 10.96.0.1' kubeadm.yaml
sed -i -e '5s/^/    /' kubeadm.yaml
mkdir ~/certs
sudo mv /etc/kubernetes/pki/apiserver.{crt,key} ./certs
sudo kubeadm init phase certs apiserver --config kubeadm.yaml
APIPID=`sudo docker ps | grep kube-apiserver | grep -v pause | cut -d " " -f 1`
sudo docker kill $APIPID

