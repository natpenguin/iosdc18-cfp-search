#
# Dockerイメージをビルドして、GCRにpush
#

# build
docker build -t gcr.io/iosdc-2018-cfp-staging/web .

# push
gcloud docker -- push gcr.io/iosdc-2018-cfp-staging/web # TODO: `gcloud docker`は非推奨らしいので変更したほうが良い
