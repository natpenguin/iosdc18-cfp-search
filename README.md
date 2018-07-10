# iosdc18-cfp-search-api

A api provides data of cfp that proposed from engineers as list

## How To Setup

```
$ git clone git@github.com:natpenguin/iosdc18-cfp-search-api.git
$ cd iosdc18-cfp-search-api
$ pip3 install -r requirements.txt -c constraints.txt
$ gunicorn api:app
```

## Lint

please specify a any file to `target.py` .
```
$ pip3 install -r requirements.txt -c constraint.txt
$ pep8 target.py
```

## Run on docker

```bash
docker-compose up
```
