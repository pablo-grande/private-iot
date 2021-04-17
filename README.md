matrix homesever
===


**Some base images were changed**

## Install

```
docker network create nginx_server
```

1. Go to reverse-proxy and run `docker-compose up`
2. Go to synapse and first run `docker-compose run --rm synapse generate`
3. Edit (with sudo) generated data/homeserver.yaml with desired config
4. Up with docker-compose up
5. Go to `localhost` (no port)

## Register a new user
Enter synapse service
```
docker-compose exec synapse register_new_user -c data/homesever.yaml https://localhost:8008
```

You can now login with

```
curl -XPOST -d '{"type": "m.login.password", "user": "<user>", "password": "<password>"}' "localhost:80/_matrix/client/r0/login"
```
It will return an `access_token`

## Element WIP
Download sample config:
```
wget https://develop.element.io/config.json -O element-config.json
```
Check Element service IP with `docker inspect <container>`

## References
[How to Install Matrix Synapse Homeserver Using Docker](https://linuxhandbook.com/install-matrix-synapse-docker/)  
[Testing the matrix.org client-server API](https://gist.github.com/RickCogley/69f430d4418ae5498e8febab44d241c9)  
[Martix.org - Client Server API](https://matrix.org/docs/guides/client-server-api)
