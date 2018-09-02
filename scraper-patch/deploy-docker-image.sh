#!/bin/bash -eu
cd `dirname $0`

TAG=0.0.2

#
# Dockerイメージをビルドして、GCRにpush
#

IMAGE=gcr.io/iosdc-2018-cfp-miya/scraper-patch:$TAG

# build
docker build -t $IMAGE .

# push
docker push $IMAGE
