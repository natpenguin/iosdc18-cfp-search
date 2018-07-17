#!/bin/bash -eu

SCRAPER_TAG='0.2.0'

if [ "`git branch`" == 'release' ]; then
    TAG=`git describe --tags`
else
    TAG="`git rev-parse --short HEAD`-stg"
    SCRAPER_TAG="${SCRAPER_TAG}-stg"
fi

echo '------------------------------'
echo "Tag: $TAG"
echo "Tag(Scraper): $SCRAPER_TAG"
echo '------------------------------'

#
# Build docker images and push to GCR
#
./scraper/deploy-docker-image.sh $TAG
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
sed -i '' "s/{{TAG}}/$TAG/" ./web/web-deployment.yaml
kubectl apply -f ./web/web-deployment.yaml
kubectl apply -f ./web/web-service.yaml

# nginx
sed -i '' "s/{{TAG}}/$TAG/" ./nginx/nginx-deployment.yaml
kubectl apply -f ./nginx/nginx-deployment.yaml
kubectl apply -f ./nginx/nginx-service.yaml

# scraper
sed -i '' "s/{{TAG}}/$SCRAPER_TAG/" ./scraper/job-scraper.yaml
kubectl apply -f ./scraper/job-scraper.yaml
