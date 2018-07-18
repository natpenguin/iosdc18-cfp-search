#!/bin/bash -eu
cd `dirname $0`

if [ $# -ne 1 ]; then
    echo "Please set args that tag."
    exit 1
fi
TAG=$1

#
# Dockerイメージをビルドして、GCRにpush
#

IMAGE=gcr.io/iosdc-2018-cfp/nginx:$TAG

# build
docker build -t $IMAGE .

# push
gcloud docker -- push $IMAGE
