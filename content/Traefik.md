---
title: Traefik Proxy
---

## Configuration
In traefik there are different approaches to declare your configuration.
Configuration is always received through a so named provider. Right now I have experience with two of the four categories of providers.

The label based configuration on might be the easiest. Just add `traefik.`-labels to the service in your compose file and you are good to go.
A basic configuration for a nginx-webserver with http and https enabled, looks like this:
```yaml

services:
    my-webserver:
        image: "nginx:bookworm"
        container_name: "static-wiki"
        volumes:
          - /opt/static-wiki/public/:/usr/share/nginx/html
        labels:
        traefik.enable: true
        # http
        traefik.http.routers.checklist.rule: PathPrefix(`/wiki`)
        traefik.http.routers.checklist.entrypoints: web
        # https
        traefik.http.routers.checklist-secure.tls: true
        traefik.http.routers.checklist-secure.rule: PathPrefix(`/wiki`)
        traefik.http.routers.checklist-secure.entrypoints: websecure
        networks:
        - traefik-net
```
Traefik detects that port 80 of the container is open and therefore creates a service. The naming of the service can get a little ugly.
Also, for me this kind of syntax isn't very clear.

The same configuration can be declared through the file based provider: an entry in the dynamic-config-file. It looks like this:
```yaml
http:
  routers:
    # http
    my-webserver:
      entrypoints: web
      rule: PathPrefix(`/my-unsafe-webserver`)
      service: nginx
    # https
    my-webserver-secure:
      entrypoints: websecure
      rule: PathPrefix(`/my-super-secured-webserver`)
      service: nginx
      tls: {}
  services:
    nginx:
      loadBalancer:
        servers:
          - url: "http://my-webserver:80"
```
Because this is declared in the dynamic-config-file, you won't need to restart the container to make it work.

## Basic Configuration

```yaml
version: "3.3"

services:

  traefik:
    image: "traefik:v3.3"
    container_name: "traefik"
    command:
      #- "--log.level=DEBUG"
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entryPoints.web.address=:80"
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

  # Declare your services below

  checklist:
    image: "hmaierdev/checklist-tool:latest"
    container_name: "checklist"
    volumes:
        - '/opt/checklist-tool/sqlite.db:/root/sqlite.db'
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.checklist.rule=Host(`localhost`) && PathPrefix(`/checklist`)"
      - "traefik.http.routers.checklist.entrypoints=web"
```


### Resources

- https://doc.traefik.io/traefik/user-guides/docker-compose/basic-example/
- https://doc.traefik.io/traefik/getting-started/quick-start/

## API

The API is reachable over port 8080. These are the available endpoint over GET:

- https://doc.traefik.io/traefik/operations/api/#dashboard


## Authentik with Traefik

- https://docs.goauthentik.io/docs/add-secure-apps/providers/proxy/server_traefik
