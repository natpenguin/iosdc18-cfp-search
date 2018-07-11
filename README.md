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
## Environment variable
* Host of MongoDB  
 `"CFP_MONGO_HOST"`
 
* Port of MongoDB  
 `"CFP_MONGO_PORT"`
 
## MongoDB
* Database name
  * before adopting cfps
    * `"iosdc2018_phase_0"`
  * after adopting cfps
    * `"iosdc2018_phase_1"`
* Collection name
    * `"cfps"`
* Document scheme
  ```python
    [{
    "title": String,
    "user": String,
    "talk_type": String,
    "description": String,
    "icon_url": String,
    "twitter_id": String
}]
  ```

 
