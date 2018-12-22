#!/bin/bash -xe

cd `dirname $0`

#
# clean
#
if [ -d '../public' ]; then
    rm -r ../public
fi
mkdir ../public

#
# save latest api response on local k8s
#
if [ -d '../tmp/volume' ]; then
    rm -r ../tmp/volume
fi
./deploy-local-k8s.sh
mkdir -p ../public/api/v1/
curl -o ../public/api/v1/proposals.json http://localhost/api/v1/proposals
./destroy-local-k8s.sh

#
# copy resources
#
cp ../nginx/index.html ../public
cp -r ../nginx/assets ../public

#
# deploy
#
firebase deploy
