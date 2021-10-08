# Django Web App - Mimic Production
This repo mimics production environment in which Django app runs.

## Setup and run the environment
To setup the environment and run the Django app, execute the following command:
```console
docker-compose up
```
As the result, the following happens:
- PostgreSQL db runs in myapp_db container
- NGINX run as a reverse proxy inside myapp_nginx container
- Redis runs as mem-cache for the django app inside myapp_redis container
- finally Gunicorn server executes the Django app inside myapp_web container

To use the app, send requests to `127.0.0.1:8083`.

Press `CTRL+C` once and wait untill all containers are stopped gracefully.
If you're impatient, press `CTRL+C` twice.

## CI
This repo specifies a Django workflow that enables some sort of basic CI/CD.
In this case, Django app uses separate test sqlite db.


## Monitoring Containers Separately

### Access to PostgreSQL DB
The following command can be used to investigate the PostgreSQL db.
```console
# enter the container
docker exec -it myapp_db bash
# authenticate as pg user (enter password)
psql -h localhost -p 5432 -U postgres -W
# listing tables 
\d 
# see the content of an arbitraty table
SELECT * FROM prodavnice_kasa;
```

### Access to Redis mem-cache
To investigate the content of Redis mem-cache, execute the following commands:
```console
# enter redi container
docker exec -it myapp_redis bash
# use redis-cli to inspect
redis-cli
# check cache size
dbsize
# list all keys
keys *
# flush all cached keys
FLUSHALL
```

### Other useful docker-compose commands

It is possible to order the docker-compose to build myapp_web the container :
```console
docker-compose up --build
```
If all containers should be recreated, then execute:
```console
docker-compose up --build --force-recreate
```

To see more information about docker-compose, check 
[the official documentation](https://docs.docker.com/compose/).

An interesting example that uses docker-compose and introduces log monitoring
can be found [here](https://github.com/MilosSimic/logging-app).

