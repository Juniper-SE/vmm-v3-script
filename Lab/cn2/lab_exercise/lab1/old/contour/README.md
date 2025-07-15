# installing Contour as ingress controller

1. Please refer to this [documentation](https://projectcontour.io/getting-started/)

2. On node **master**, download contour controller manifest file, 


        curl -O -L  https://projectcontour.io/quickstart/contour.yam


4. Install contour as ingress 

        kubectl apply -f contour.yaml

5. Verify that ingress controller installed

        kubectl get ns
        kubectl get pods -n  projectcontour
        kubectl get svc -n projectcontour <--- this is to verify that floating ip has been assigned to the ingress controller

6. Contour ingress controller is installed
