#!/bin/bash -eu

#
# Build docker images and push to GCR
#
./scraper/deploy-docker-image.sh
./web/deploy-docker-image.sh
./nginx/deploy-docker-image.sh

#
# Apply k8s configurations
#

# mongo
kubectl apply -f ./mongo/mongo-volumeclaim.yaml
kubectl apply -f ./mongo/mongo-replicaset.yaml
kubectl apply -f ./mongo/mongo-service.yaml

# scraper
kubectl apply -f ./scraper/job-scraper.yaml

# web
kubectl apply -f ./web/web-deployment.yaml
kubectl apply -f ./web/web-service.yaml

# nginx
kubectl apply -f ./nginx/nginx-deployment.yaml
kubectl apply -f ./nginx/nginx-service.yaml
