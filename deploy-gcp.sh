#!/bin/bash -eu

if [ "`git rev-parse --abbrev-ref HEAD`" == 'release' ]; then
    echo "Start deploy to [Production]"
    TAG=`git describe --tags`
    NGINX_SERVICE_TYPE='NodePort'
else
    echo "Start deploy to [Staging]"
    TAG="`git rev-parse --short HEAD`-stg"
    NGINX_SERVICE_TYPE='LoadBalancer'
fi

echo '------------------------------'
echo "Tag: $TAG"
echo '------------------------------'

#
# Build docker images and push to GCR
#
./web/deploy-docker-image.sh $TAG
./nginx/deploy-docker-image.sh $TAG

#
# Apply k8s configurations
#

# mongo
kubectl apply -f ./mongo/mongo-volumeclaim.yaml
kubectl apply -f ./mongo/mongo-replicaset.yaml
kubectl apply -f ./mongo/mongo-service.yaml

# web
sed -i "s/{{TAG}}/$TAG/" ./web/web-deployment.yaml
kubectl apply -f ./web/web-deployment.yaml
kubectl apply -f ./web/web-service.yaml

# nginx
sed -i "s/{{TAG}}/$TAG/" ./nginx/nginx-deployment.yaml
sed -i "s/{{TYPE}}/$NGINX_SERVICE_TYPE/" ./nginx/nginx-service.yaml
kubectl apply -f ./nginx/nginx-deployment.yaml
kubectl apply -f ./nginx/nginx-service.yaml
