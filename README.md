Private-IoT
===

Send IoT data over Tor. Register in easily extendable Matrix homeserver.

## Tor Setup
> Look _How to Make Requests Over Tor Browser Using Python_ ref.

Having install tor. Go to /etc/tor/torrc and edit these lines:
```
ControllerPort 9051
HashedControlPassword <password>
CookieAuthentication
```
Create a new <password> with
```
tor --hash-password "passphrase"
```
This configuration will let our computer form part of the Tor relay and do something like:

It is important to **restart tor service**, sometime it gets faulty when starting new connections
```
sudo systemctl restart tor
```

```
import requests

session = requests.session()
session.proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

session_obj = session.get("http://onionshare:gentleman-nurture@v5eiiowe25r6ukd7dofpvkksix3v25mmyuiaqtunz53sjaciy2juatyd.onion")

```

## Pacemaker
Simple Arduino code for ESP32 chip that sends health data every 10s simulating a pacemaker.

## MQTT
Contains a mosquitto server and an MQTT subscribber. Currently listens to every topic there and sends whatever it listens to Matrix homeserver


## Matrix homesever

Follow the given instructions of official [Martix.org - INSTALL.md](https://github.com/matrix-org/synapse/blob/master/INSTALL.md)

We used python pip to install a Matrix homeserver running in localhost:8008. 
Start homeserver with `synctl start`.  
Users were manually added with `register_new_matrix_user` command.  
1. Admin user creates a room
2. Normal user
3. Admin invites normal user to join room
4. Normal user can send information to room through Matrix client from Python SDK.

*Register user and room creation should be done through Matrix client in one bit*

*Would be nice to [federate](https://github.com/matrix-org/synapse/blob/master/docs/federate.md)

### Install with docker and docker-compose
**Some base images were changed**


```
docker network create nginx_server
```

1. Go to reverse-proxy and run `docker-compose up`
2. Go to synapse and first run `docker-compose run --rm synapse generate`
3. Edit (with sudo) generated data/homeserver.yaml with desired config
4. Up with docker-compose up
5. Go to `localhost` (no port)

### Register a new user
Enter synapse service
```
docker-compose exec synapse register_new_matrix_user -c data/homesever.yaml http://localhost:8008
```

You can now login with

```curl
curl -XPOST -d '{"type": "m.login.password", "user": "<user>", "password": "<password>"}' "localhost:80/_matrix/client/r0/login"
```
It will return an `access_token`


### Element WIP
Download sample config:
```
wget https://develop.element.io/config.json -O element-config.json
```
Check Element service IP with `docker inspect <container>`


## References
[How to Install Matrix Synapse Homeserver Using Docker](https://linuxhandbook.com/install-matrix-synapse-docker/)  
[Testing the matrix.org client-server API](https://gist.github.com/RickCogley/69f430d4418ae5498e8febab44d241c9)  
[Martix.org - Client Server API](https://matrix.org/docs/guides/client-server-api)  
[Send data from ESP8266 or ESP32 to Raspberry Pi via MQTT](https://diyi0t.com/microcontroller-to-raspberry-pi-wifi-mqtt-communication/)
[How to Make Requests Over Tor Browser Using Python](https://hackernoon.com/how-to-make-requests-over-tor-browser-using-python-zp153ur0)

(https://hub.docker.com/r/strm/tor-hiddenservice-nginx)
(https://hub.docker.com/r/marcelmaatkamp/tor-hidden-service) -> hello-world en vez de hello_world
(http://containertutorials.com/docker-compose/flask-simple-app.html)
(https://github.com/cmehay/docker-tor-hidden-service)
