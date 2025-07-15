# Installing analytic on k8s + CN2
In this lab exercise, analytic will be installed on k8s + CN2.

Documentation on how to install analytics on k8s + CN2, can be found [here](https://www.juniper.net/documentation/us/en/software/cn-cloud-native22/cn-cloud-native-k8s-install-and-lcm/cn-cloud-native-upstream-install-and-lcm/topics/task/cn-cloud-native-k8s-install-analytics.html)

## Installing contrail analytics

1. Download analytics deployer manifest file from [here](https://support.juniper.net/support/downloads/?p=contrail-networking)
2. extract the analytics manifest file

        tar xvfz contrail-analytics-<version>.tgz
3. Create a namespace **contrail-analytics**

        kubectl create ns contrail-analytics

4. Extract file **image-pull-secret-values.yaml** from the contrail analytics package

        tar xvfz contrail-analytics-<version>.tgz contrail-analytics/image-pull-secret-values.yaml
5. Check on the k8s cluster if secret to access hub.juniper.net has been configured. it may be called **registrypullsecret**. it was created during the CN2 installation

        kubectl get secret -n contrail-analytics | grep registrypullsecret

6. Edit file contrail-analytics/image-pull-secret-values.yaml, edit entry **imagePullSecrets** with the secret from previous step

        cat contrail-analytics/image-pull-secret-values.yaml
        sed -i -e 's/_SECRET_NAME_/registrypullsecret/' contrail-analytics/image-pull-secret-values.yaml
        contrail-analytics/image-pull-secret-values.yaml
7. If helm is not installed, install it first,
8. Install contrail analytics using helm

        helm -n contrail-analytics install analytics contrail-analytics-<version>.tgz -f image-pull-secret-values.yaml

9. To verify contrail analytics installation 

        helm -n contrail-analytics list

10. Get the externalIP assigned to contrail analytics

        kubectl -n contrail-analytics get services

## installing lens
1. Download Kubernetes Lens GUI from [here](https://k8slens.dev/)
2. Download CN2 extension for Lens GUI from [here](https://github.com/Juniper/contrail-networking/tree/main/lens-extension)
3. Install Lens on your workstation.
4. open Lens Application, and install the CN2 extension
5. Open catalog and access the kubernetes cluster

## Accessing CN2 introspect
1. On your workstation, open kubectl proxy, and keep this session open 

        kubectl proxy 

2. On your workstation, open web browser to this url http://127.0.0.1:8001/apis/introspect.k8s.io/v1beta1/index



