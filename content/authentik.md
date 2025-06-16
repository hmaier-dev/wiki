---
title: Authentik
description: An open source identity provider
---

### Installation
Is kinda straight forward:

- https://docs.goauthentik.io/docs/install-config/install/docker-compose

## Bootstraping
When deploying to public space you can use these variables at the `worker`-container to
skip the OOB-experience:

- `AUTHENTIK_BOOTSTRAP_PASSWORD`
- `AUTHENTIK_BOOTSTRAP_TOKEN`
- `AUTHENTIK_BOOTSTRAP_EMAIL`

By the way: The default user is call `akadmin`.

Refernece: https://docs.goauthentik.io/docs/install-config/automated-install

## Middleware in Traefik

Reference: 
- https://docs.goauthentik.io/docs/add-secure-apps/providers/proxy/server_traefik
- https://github.com/brokenscripts/authentik_traefik

