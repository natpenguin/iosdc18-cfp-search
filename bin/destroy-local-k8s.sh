#!/bin/bash

cd `dirname $0`

#
# Cluster
#

kubectl delete -f ./kubernetes/cluster.yaml

#
# Jobs
#

kubectl delete -f ./kubernetes/job-scraper.yaml
kubectl delete -f ./kubernetes/job-scraper-patch.yaml

#
# Finish
#

echo 'Kubernetes cluster will destroyed.'
