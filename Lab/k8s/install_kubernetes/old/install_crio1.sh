sudo apt -y update
sudo apt -y upgrade
sudo apt-get install -y apt-transport-https ca-certificates curl

sudo apt -y install cri-o cri-o-runc
sudo systemctl daemon-reload
sudo systemctl enable crio --now
sudo apt-get install -y kubelet=1.21.2-00 kubeadm=1.21.2-00 kubectl=1.21.2-00
# sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl cri-o cri-o-runc