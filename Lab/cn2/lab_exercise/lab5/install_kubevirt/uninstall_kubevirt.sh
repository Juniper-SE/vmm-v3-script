#!/bin/bash
# rm kubevirt-operator.yaml
# rm kubevirt-cr.yaml
export KUBEVIRT_VERSION=v0.58.0
echo "Kubevirt version ${KUBEVIRT_VERSION}"
# curl -O -L https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-operator.yaml
# curl -O -L https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-cr.yaml
kubectl delete -f https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-cr.yaml
kubectl delete -f https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-operator.yaml

