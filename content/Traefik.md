---
title: Traefik
description: Web-Application-Proxy for containers
---
## General Configuration
In Traefik the configuration is done in two different ways:

- static configuration
- dynamic configuration

The static config can be though of as an startup config. It sets the connections to the different provides (file, docker, etc.) and 
sets the entrypoints (often just port 80 and 443). When something in this config changes, the traefik container needs to get restarted.
Usally this _should not_ happend often, because the values are mostly constant.
You need to tell Traefik where it is when starting:
```yaml
services:
  traefik:
    command:
      - "--configFile=/etc/traefik/traefik.yaml"
    volumes:
      - "./traefik.yml:/etc/traefik/traefik.yml:ro"
```

The dynamic config is the way, how the magic _can_ happens. Traefik uses different provides to get its routes, services and rules.
The least magically way is to use the [file-provider](https://doc.traefik.io/traefik/providers/file/).
You need to tell Traefik the dir to look for it:
```yaml
providers:
  file:
    directory: "/rules"
    watch: true
```
Make sure to mount it in the `docker-compose.yml`:
```yaml
services:
  traefik:
    volumes:
      - "./rules:/rules"
```

## Dynamic Configuration Types
In traefik there are different approaches to declare your configuration.
Configuration is always received through a so named provider. Right now I have experience with two of the four categories of providers.

### Label based (Docker)
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

### Files based
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

## Project Example
I like to go for the file-based dynamic configuration. Meaning, I create a separate directory called `./rules`
which I mount into the container. For every service I create a separate file.

```bash
.
├── apps            ## Services plus their config
│   ├── authentik
│   │   └── compose.yml
│   └── outline
│       └── compose.yml
├── compose.yml     ## Traefik compose
├── LICENSE
├── README.md
├── rules           ## Dynamic Config
│   ├── authentik.yml
│   └── outline.yml
└── traefik.yml     ## Static Config
```

## Certificates

Self signed certs

https://doc.traefik.io/traefik/expose/docker/#create-a-self-signed-certificate

## Resources
- https://doc.traefik.io/traefik/user-guides/docker-compose/basic-example/
- https://doc.traefik.io/traefik/getting-started/quick-start/

## API

The API is reachable over port 8080. These are the available endpoint over GET:

- https://doc.traefik.io/traefik/operations/api/#dashboard

## Templating
When you want deploy a lot of services but you don't want to type all of them out,
you could use _Go Templating_.

- https://doc.traefik.io/traefik/providers/file/#go-templating

## Configuration Examples
### Webserver with HTTPS
```yaml
http:
  routers:
    website:
      entrypoints:
        - web
        - websecure
      rule: Host(`www.mysite.com`) || Host(`mysite.com`)
      service: website
      tls: {}
  services:
    website:
      loadBalancer:
        servers:
          - url: "http://website:8080"
~
```
