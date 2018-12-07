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
if [ -d '../tmp' ]; then
    rm -r ../tmp
fi
./deploy-local-k8s.sh
curl -o ../public/api.json http://localhost/api
./destroy-local-k8s.sh

#
# copy resources
#
cp ../nginx/index.html ../public
cp -r ../nginx/assets ../public

#
# change endpoint
#
sed -i '' "s|axios.get('/api')|axios.get('/api.json')|" ../public/assets/index.js

#
# deploy
#
firebase deploy
