#!/bin/bash -eu
cd `dirname $0`

IMAGE=scraper-job-patch-rejectcon

docker build -t $IMAGE .
docker run --net='iosdc18-cfp-search_default' $IMAGE
