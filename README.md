# Gateway

Whole Gateway can be started from this single repository with docker-compose.


## Services and routing

| Service | Path |
| --- | --- |
| Voting service | `/voting-service-api/` |
| Synchronization service | `/synchronization-service-api/` |
| Voting process manager | `/voting-process-manager-api/` |
| Token manager | `/token-manager-api/` |
| State vector | `/statevector/` |
| _config.json_ | `/statevector/config/config.json` |
| _datamodels.yaml_ | `/statevector/config/datamodels.yaml` |

In default development environment Gateway exposes main `nginx proxy` on port `8080` and `vote-db` on port `8223`.


### Staging environment

In staging, Gateway's nginx proxy is exposed at port `8101` for host machine. DB stays on `8223`.

Every route is prefixed with `/gateway`. E. g. [voting-service on stage](https://team17-21.studenti.fiit.stuba.sk/gateway/voting-service-api/docs).


## Requirements

`docker-compose.yml` uses version `"3.8"`, which means that required versions are: `docker >= 19.03.0` and `docker-compose >= 1.25.5`.

Installed versions can be checked with `docker -v` and `docker-compose -v`.


## How to run it

```
docker-compose up -d --build
```

This uses the base file: `docker-compose.yml`.

Optional `-p` flag sets name prefix for containers. Otherwise it defaults to working directory's name. Might be used to create shorter container names, e.g. `docker-compose -p g up -d --build` runs development environment but prefixes all containers with `g` insted of `gateway`.

### Pro tip

You can stop and remove containers and networks with `down` command. For the base compose run this command while in `gateway/` directory:

```
docker-compose down
```

Or specify `project-name` of the docker-compose:

```
docker-compose -p gtest-sync down
```


## Testing in Docker

Check service's `test.env` file. Then run with (example for synchronization-service):

```
docker-compose --env-file synchronization-service/test.env up --build --exit-code-from synchronization-service --renew-anon-volumes
```

Shorter command can be used:

```
docker-compose --env-file synchronization-service/test.env up --build --renew-anon-volumes
```

| Flag | Description |
| --- | --- |
| `--renew-anon-volumes` | tells docker to recreate containers with clean anonymous volumes (their disks) to make sure they are all perfectly clean for testing. |
| `--exit-code-from synchronization-service` | specifies container to get exit code (the number) from. This is necessary in GH pippeline but can be ommited when testing locally - then you need to read the pytest's conclusion in logs. |
| `--build` | makes sure every container is built to the newest version (which sometimes isn't the case without this flag). |
| `--env-file` | specifies which `.env` file to use. For example see [synchronization-service/test.env](synchronization-service/test.env). |


### Be aware

Don't include `-d` flag in testing. If you exclude the flag, you will be served logs from all caontainers immediately after containers are created so there will be no need to run any other command to see how tests are doing.

If you exclude `--exit-code-from` flag, you will need to send SIGINT after tests are done in order to stop containers and close thar docker-compose session. In other words, press `Ctrl+C` after tests are done.


## E2E Tests

Command:
```
docker-compose -f docker-compose.e2etest.yml up -d --build --renew-anon-volumes
```

| Flag |D escription |
| --- | --- |
|    `-f`          |            file to use|
|    `--renew-anon-volumes`   | don't reuse some used cached volumes - get us fresh clean database |

In file `docker-compose.e2etest.yml`:

Set `ACCEPT_VALID_TOKEN=1`, if you want to accept "valid" token.
But it isn't relevant now that e2e tests should use real tokens.

Lines 108 and 109 can be commented out / deleted if no direct connection from host to DB is required. 
If you want to connect to this DB from your host, be aware it uses the same `8223` port as the traditional gateway local build.
In general, this compose can't be run while the traditional `docker-compose.yml` is running, because it uses the same `8223` and `8080` ports.
If you need to run bouth simultaneously for whatever reason, perhaps change ports in one of them.
But this situation shouldn't be relevant.

