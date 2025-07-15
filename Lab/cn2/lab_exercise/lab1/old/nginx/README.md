# installing NGIX as ingress controller

1. Please refer to this [documentation](https://kubernetes.github.io/ingress-nginx/deploy/#bare-metal)

2. On node **master**, download NGIX controller manifest file, 


        curl -O -L https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.1/deploy/static/provider/cloud/deploy.yaml


3. deploy NGIX as ingress controlller

        kubectl apply -f deploy.yaml

4. Verify that ingress controller installed

        kubectl get pods -n ingress-nginx
        kubectl get svc -n ingress-nginx  <--- this is to verify that floating ip has been assigned to the ingress controller

5. NGINX ingress controller is installed
