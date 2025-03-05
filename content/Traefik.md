---
title: Traefik Proxy
---

## TL;DR

- Restart individual service: `docker compuse up -d <service>`

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
