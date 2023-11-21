sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt -y update
sudo apt -y upgrade
#sudo apt-get install -y docker-ce docker-ce-cli containerd.io wget python2.7
sudo apt-get install -y docker-ce docker-ce-cli containerd.io wget #python-is-python3
# sudo apt-get install -y docker.io
sudo usermod -a -G docker ubuntu
# sudo reboot


