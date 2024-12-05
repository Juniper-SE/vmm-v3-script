yum -y update
yum -y upgrade
yum -y install epel-release git net-tools sshpass tmux
curl -O  https://bootstrap.pypa.io/pip/2.7/get-pip.py
chmod +x get-pip.py
python ./get-pip.py
pip install  ansible==2.7.18

