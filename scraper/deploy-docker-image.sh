#!/bin/bash -eu
cd `dirname $0`

#
# Dockerイメージをビルドして、GCRにpush
#

TAG=gcr.io/iosdc-2018-cfp-staging/scraper:0.1.0

# build
docker build -t $TAG .

# push
gcloud docker -- push $TAG
