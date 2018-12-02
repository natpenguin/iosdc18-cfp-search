#!/bin/bash

cd `dirname $0`

#
# Build docker images
# 

docker build -t iosdc-web ../web
docker build -t iosdc-nginx ../nginx
docker build -t iosdc-scraper ../scraper
docker build -t iosdc-scraper-patch ../scraper-patch

#
# Cluster
#

# volume
VOLUME_PATH="$(cd ../; pwd)/tmp/volume"
sed -i '.bak' "s|{{VOLUME_PATH}}|$VOLUME_PATH|" ./kubernetes/cluster.yaml

# cluster
kubectl apply -f ./kubernetes/cluster.yaml

# wait for mongo
echo 'Wait for launch mongo ...'
kubectl wait --for condition=ready --timeout=120s pod --selector app=mongo

#
# Jobs (need batch apply)
#

# scraper (phase 2)
echo 'Wait for complete job.batch/scraper-phase2 ...'
kubectl apply -f ./kubernetes/job-scraper.yaml
kubectl wait --for=condition=complete --timeout=120s job.batch/scraper-phase2

# scraper patch
echo 'Wait for complete job.batch/patch-v3 ...'
kubectl apply -f ./kubernetes/job-scraper-patch.yaml
kubectl wait --for=condition=complete --timeout=120s job.batch/patch-v3

#
# Finish
#

echo 'Please access to http://localhost/'
