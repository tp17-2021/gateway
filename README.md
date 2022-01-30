# Gateway

All Gateway services can be started from this single repository with docker-compose.


#### Submodules

We ditched them.


## Requirements

`docker-compose.yml` uses version `"3.8"`, which means that required versions are: `docker >= 19.03.0` and `docker-compose >= 1.25.5`.

Installed versions can be checked with `docker -v` and `docker-compose -v`.


## How to run it

```
docker-compose -p g up -d --build
```

This uses the base file: `docker-compose.yml`. The `-p` flag sets name prefix for containers.


## Testing in Docker

For now, only `synchronization-service` has some tests ready. Ca nbe run with:

```
docker-compose -f docker-compose.test.yml -f docker-compose.test.synchronization-service.yml -p g-test up --build --exit-code-from synchronization-service --force-recreate --remove-orphans
```
