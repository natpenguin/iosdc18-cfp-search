#!/bin/bash -eu
cd `dirname $0`

IMAGE=scraper

docker build -t $IMAGE .
docker run --net='iosdc18-cfp-search_default' $IMAGE
