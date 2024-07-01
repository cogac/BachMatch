#!/bin/bash

# Check if Minikube is running
minikube status &> /dev/null
if [ $? -ne 0 ]; then
    echo "Minikube is not running. Start it first."
    exit 1
fi
echo 'Minikube is started and will get used'

# Check if Strimzi Operator is running
kubectl get strimzioperators -n strimzi-system &> /dev/null
if [ $? -ne 0 ]; then
    echo "Strimzi Operator not found. Install it."
    kubectl apply -f https://raw.githubusercontent.com/strimzi/strimzi-kafka-operator/0.41.0/examples/kafka/kafka-ephemeral-single.yaml
fi

# Check if Hadoop Cluster is running
helm status my-hadoop-cluster 2>&1 >> /dev/null 2>&1 || echo "The hadoop cluster needs to start first (wait time 2 minutes) -- disregard any error messages regarding it" && \
    helm install --wait --timeout 2m0s \
        my-hadoop-cluster pfisterer-hadoop/hadoop \
        --set hdfs.dataNode.replicas=3  \
        --set yarn.nodeManager.replicas=3
 


# Start the cluster with skaffold dev
# Initialize counter for log file
id=1

# Check if a log file exists, increment id until one is found
while [ -e "skaffold_log${id}.log" ]; do
    ((id++))
done
echo "Using log file skaffold_log${id}.log to log skaffold"
# Run skaffold dev with the newly generated log file name
skaffold dev > "skaffold_log${id}.log" &
echo 'Test'
