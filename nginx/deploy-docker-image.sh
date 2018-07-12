#!/bin/bash -eu
cd `dirname $0`

#
# Dockerイメージをビルドして、GCRにpush
#

TAG=gcr.io/iosdc-2018-cfp-staging/nginx

# build
docker build -t $TAG .

# push
gcloud docker -- push $TAG
