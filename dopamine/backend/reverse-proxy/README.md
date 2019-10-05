# Nginx reverse proxy in Docker

### Description

> WARNING
> It now only works on MAC OS X because of how docker internal routing is implemented

`.env` file contains ENV variable for image and container name


`conf.d/default.conf` file contains nginx http server config for the following cases:
1. Backend HTTP API access with all needed directives with 8081 port
2. Backend Websocket API with all needed directives and HTTP headers
3. Frontend API with 8080 port

Ports can be changed inside the file as well as routing settings

### Usage

run `./build_proxy.sh` to build container and start proxy

run `./clean_proxy.sh` to stop proxy and remove container
