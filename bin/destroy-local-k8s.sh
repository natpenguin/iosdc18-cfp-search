#!/bin/bash -xe

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
# Temporary directory (volumes)
#
if [ -d '../tmp/volume' ]; then
    rm -r ../tmp/volume
fi

#
# Finish
#

echo 'Kubernetes cluster will destroyed.'
