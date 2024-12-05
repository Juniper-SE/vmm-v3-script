# contrail firewall policy
1. Create the services and pods for this lab

        kubectl apply -f lab3_backendyaml
2. Create policy1, to allow traffic to dbserver from webserver10 only

        kubectl apply -f lab3_policy1.yaml

3. Create policy2, to allow traffic to dbserver from 10.1.12.0/24 only

        kubectl apply -f lab3_policy2.yaml
4. Create policy3, to prevent dbserver from initiation outgoing traffic

        kubectl apply -f lab3_policy3.yaml

        
