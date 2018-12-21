# この素晴らしいCfPに祝福を！

[https://iosdc-cfps.penginmura.tech/](https://iosdc-cfps.penginmura.tech/)
![screenshot](doc/image/screenshot.png)

## How To Setup

### Run on docker

Start containers:

```bash
docker-compose up -d
# Hot-reload is enabled on default, so you don't need restart containers in most case.
```

Setup data via scraper:

```bash
./setup-local.sh
```

### Run on Kubernetes (but no synchronize to host files on realtime)

#### Deploy

```bash
./bin/deploy-local-k8s.sh
```

**Note:**
This script creates local volume to `./tmp/volume`.

#### Destroy

```bash
./bin/destroy-local-k8s.sh
```

**Note:**
All volumes delete too.

## Lint

please specify a any file to `target.py` .
```
$ pip3 install -r requirements.txt -c constraint.txt
$ pep8 target.py
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
    "detail_url": String,
    'talk_date': ISODate,
    'talk_site': String,
    'is_adopted': Bool
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

## Deploy to Firebase

```sh
./bin/deploy-firebase.sh
```

## API

Defined api specification in [doc/swagger.yaml](doc/swagger.yaml) by OpenAPI.

[http://localhost:8080/](http://localhost:8080/)

## Reference

| name | link |
|-------|-------|
|vue.js | https://jp.vuejs.org https://www.vuemastery.com |
|Bulma | https://bulma.io |
| fontawesome | https://fontawesome.com |
| mongoDB | https://docs.mongodb.com/manual/ https://utage.headwaters.co.jp/blog/?p=5065 |
