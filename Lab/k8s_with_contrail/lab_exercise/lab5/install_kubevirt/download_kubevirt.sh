rm kubevirt-operator.yaml
rm kubevirt-cr.yaml
export KUBEVIRT_VERSION="v0.48.0"
curl -O -L https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-operator.yaml
curl -O -L https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-cr.yaml
