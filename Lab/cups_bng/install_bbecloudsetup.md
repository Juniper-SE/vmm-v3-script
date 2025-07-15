# This document provide guideline on how to install bbecloud setup

## Nodes in the lab

deployer: jump host to run the installation script
node1, node2, node3: kubernetes nodes

## steps
1. On your workstation, run ansible playbook [update_system.yaml](linux_node/update_system.yaml) to update system software on kubernetes nodes and to create the disk partitions required by bbecloud software

        cd linux_node
        ansible-playbook update_system.yaml

2. open ssh session into node **deployer**, create new ssh key, and upload this key to the kubernetes nodes 

        ssh deployer
        ssh-keygen -f ~/.ssh/key1
        for i in ubuntu@172.16.11.11{1..3}
        do
                ssh-copy-id -i ~/.ssh/key1.pub ${i}
        done

3. upload the bbecloudsetup package into node deployer

        scp bbecloudsetup-v2.0.0.tgz deployer:~/

4. open ssh session into node deployer, and extract bbecloudsetup installation package

        ssh deployer
        tar xvfz bbecloudsetup-v2.0.0.tgz

5. create configuration template for bbecloudsetup. (copy the exampleconfig.yaml to config.yaml, and edit file config.yaml). Set the parameters inside file config.yaml

        cd bbecloudsetup
        cp exampleconfig.yaml config.yaml
        vi config.yaml

4. on node deployer, start ssh-agent and add ssh-key **key1** into the agent

        eval $(ssh-agent)
        ssh-add ~/.ssh/key1

5. on node deployer, start the installation process of bbecloudsetup

        tmux
        cd ~/bbecloudsetup
        sudo -E ./bbecloudsetup -d install -template ./config.yaml


## installing dBNG on bbecloudsetup
1. upload dbng into node deployer

        scp junos-bng-cups-controller-pkg-amd64-23.4R2.13.tgz deployer:~/

2. extract the software

        tar xvfz junos-bng-cups-controller-pkg-amd64-23.4R2.13.tgz
        
3. if python3 virtual environment is not installed, install it first. 

        sudo apt install python3-venv
4. Run **dbng_loader**

        sudo ./dbng/dbng_loader
5. Verify that dbng software is ready to be installed

        dbng version
6. Link dbng version

        sudo -E dbng link --context <cluster_name> --version <dbng version>
        sudo -E dbng link --context cp1 --version 23.4R2.13
7. login into kubernetes repository 

        docker login -u <user> <repository virtual IP>:5000
        docker login -u admin 172.16.11.11:5000

8. Run **dbng setup** to configure the installation

        sudo -E dbng setup –-context <contextName> --update [–-bbecloudsetup] [–-ssh] <host:port> [--secrets]
        sudo -E dbng setup --context cp1 --update --ssh 172.16.11.111:8200

9. Verify dbng installation

        dbng version --context cp1 --detail
10. Start dbng rollout
        sudo -E dbng rollout --context <contextName>
        sudo -E dbng rollout --context cp1


        sudo -E dbng cpi add <cpi-name> --context <context> --version <swVersion>

        sudo -E dbng cpi add cpi-test1 --context cp1 --version 23.4R2.13


         
11. Verify that dbng services are up and running

        dbng status --context <contextName> --detail
        dbng status --context cp1 --detail




## installing APM
1. upload apm file into node deployer

        scp apm-3.2.1-2.tgz deployer:~/

2. extract the software

        tar xpvfz apm-3.2.1-2.tgz

3. Run apm_loader

        sudo apm/apm_loader

4. verify that apm software is ready to be installed

        apm version

5. link apm version 
        
        sudo -E apm link --context <contextName> --version <version>

        sudo -E apm link --context cp1 --version 3.2.1-2

6. login into kubernetes repository 

        docker login -u <user> <repository virtual IP>:5000
        docker login -u admin 172.16.11.11:5000

7. run **apm setup**

        sudo -E apm setup –-context <contextNam>e --update [–-bbecloudsetup] [–-ssh] <host:port> [--secrets]

        sudo -E apm setup –-context cp1 --update –-ssh 172.16.11.111:8200

