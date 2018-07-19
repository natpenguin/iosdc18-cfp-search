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
    `"iosdc2018_phase_0"`
  * after adopting cfps  
    `"iosdc2018_phase_1"`
* Collection name  
    `"cfps"`
* Document scheme
  ```python
    [{
    "title": String,
    "user": String,
    "talk_type": String,
    "description": String,
    "icon_url": String,
    "twitter_id": String,
    "detail_url": String
    }]
  ```

## Deploy to GCP

1. Create cluster on GKE.
2. Select cluster like below.
    ```sh
    gcloud container clusters get-credentials xxxx
    ```

3. Run deploy script!

    ```sh
    ./deploy-gcp.sh
    ```
4. Wait to configure external-ip by GCP.
    ```sh
    $ ubectl get svc
    NAME         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
    kubernetes   ClusterIP      10.7.240.1     <none>        443/TCP        7m
    mongo        ClusterIP      10.7.251.115   <none>        27017/TCP      10s
    nginx        LoadBalancer   10.7.245.253   <pending>     80:32174/TCP   9s
    web          ClusterIP      10.7.248.23    <none>        8000/TCP       9s
    ```

5. Please access to binded external-ip on your browser.
    ```sh
    $ kubectl get svc
    NAME         TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)        AGE
    kubernetes   ClusterIP      10.7.240.1     <none>           443/TCP        9m
    mongo        ClusterIP      10.7.251.115   <none>           27017/TCP      2m
    nginx        LoadBalancer   10.7.245.253   35.200.125.234   80:32174/TCP   1m
    ```

    http://35.200.125.234/
