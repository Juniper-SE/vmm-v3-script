#!/bin/bash
FILE1=~/kubespray/inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml
LINENUM=`grep -n '^container_manager:' ${FILE1} | cut -d ':' -f 1`
if [ -n "${LINENUM}" ];
then
	echo found at $LINENUM
   sed -i -e "${LINENUM}d" ${FILE1}
fi
echo "container_manager: crio" | tee -a ${FILE1}
LINENUM=`grep -n '^etcd_deployment_type:' ${FILE1} | cut -d ':' -f 1`
if [ -n "${LINENUM}" ];
then
	echo found at $LINENUM
    sed -i -e "${LINENUM}d" ${FILE1}
fi
echo "etcd_deployment_type: host" | tee -a ${FILE1}
LINENUM=`grep -n '^kubelet_deployment_type:' ${FILE1} | cut -d ':' -f 1`
if [ -n "${LINENUM}" ];
then
	echo found at $LINENUM
    sed -i -e "${LINENUM}d" ${FILE1}
fi
echo "kubelet_deployment_type: host" | tee -a ${FILE1}
LINENUM=`grep -n '^enable_nodelocaldns:' ${FILE1} | cut -d ':' -f 1`
if [ -n "${LINENUM}" ];
then
	echo found at $LINENUM
    sed -i -e "${LINENUM}d" ${FILE1}
fi
echo "enable_nodelocaldns: false" | tee -a ${FILE1}
LINENUM=`grep -n '^enable_dual_stack_networks:' ${FILE1} | cut -d ':' -f 1`
if [ -n "${LINENUM}" ];
then
	echo found at $LINENUM
    sed -i -e "${LINENUM}d" ${FILE1}
fi
echo "enable_dual_stack_networks: true" | tee -a ${FILE1}
LINENUM=`grep -n '^kube_network_plugin:' ${FILE1} | cut -d ':' -f 1`
if [ -n "${LINENUM}" ];
then
	echo found at $LINENUM
    sed -i -e "${LINENUM}d" ${FILE1}
fi
echo "kube_network_plugin: cni" | tee -a ${FILE1}
LINENUM=`grep -n '^kube_version:' ${FILE1} | cut -d ':' -f 1`
if [ -n "${LINENUM}" ];
then
	echo found at $LINENUM
   sed -i -e "${LINENUM}d" ${FILE1}
fi
echo "kube_version: v1.26.3" | tee -a ${FILE1}
LINENUM=`grep -n '^cluster_name:' ${FILE1} | cut -d ':' -f 1`
if [ -n "${LINENUM}" ];
then
	echo found at $LINENUM
    sed -i -e "${LINENUM}d" ${FILE1}
fi
echo "cluster_name: k8s" | tee -a ${FILE1}

