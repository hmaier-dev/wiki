---
title: Authentik
description: An open source identity provider
---

## Installation
Is kinda straight forward:

- https://docs.goauthentik.io/docs/install-config/install/docker-compose

### `.env`-file

```bash
# ------------------------
# NOTE: this file needs to be called .env and not docker.env!
#       When named different PG_PASS cannot be set. I don't know why...
#
# --------------------------------------
# For automated install

AUTHENTIK_BOOTSTRAP_PASSWORD=qwertz1234
AUTHENTIK_BOOTSTRAP_TOKEN=
AUTHENTIK_BOOTSTRAP_EMAIL=mail@server.de
## echo "AUTHENTIK_SECRET_KEY=$(openssl rand -base64 60 | tr -d '\n')" >> .env
AUTHENTIK_SECRET_KEY=<key>

## Postgres
## echo "PG_PASS=$(openssl rand -base64 36 | tr -d '\n')" >> .env
PG_PASS=<key>
POSTGRES_USER=authentik
POSTGRES_DB=authentik
```

## Bootstraping
When deploying to public space you can use these variables at the `worker`-container to
skip the OOB-experience:

- `AUTHENTIK_BOOTSTRAP_PASSWORD`
- `AUTHENTIK_BOOTSTRAP_TOKEN`
- `AUTHENTIK_BOOTSTRAP_EMAIL`

By the way: The default user is call `akadmin`.

Refernece: https://docs.goauthentik.io/docs/install-config/automated-install

## Sitzungs Dauer einstellen
Einerseits kann man am Provider die Gültigkeit des Tokens einstellen,
andererseits kann man in der Phase (User Login Stage) die Sessionsdauer einstellen:

- https://www.reddit.com/r/Authentik/comments/1e6023h/noob_question_autologout_after_x_hours/
- https://docs.goauthentik.io/docs/add-secure-apps/flows-stages/stages/user_login/

Wie genau diese beiden Parts zusammen hängen, muss ich noch verstehen.


## ForwardAuth in Traefik
Um vor jegliche Anwendung einen Authentifizierung zu setzen, kann man Authentik in Traefik als
Middleware über ForwardAuth einbinden. Von Authentik selbst gibt es dazu eine passenden Anleitung.

- https://docs.goauthentik.io/docs/add-secure-apps/providers/proxy/server_traefik

Wichtig ist, dass `outpost.company:9000` mit dem Container-Namen des Authentik-Servers im `traefik-net` ersetzt wird.
Zum Beispiel aus `outpost.company:9000` wird `authentik-server:9000`. Dies ist der gleiche Name dem man dem Loadbalancer übergibt.

Im Authentik müssen zudem noch ein Provider und eine Application angelegt werden.
Zuletzt fügt man den Provider noch dem _Embedded Outpost_ hinzu.


Reference: 
- https://github.com/brokenscripts/authentik_traefik

## Session Duration

- https://docs.goauthentik.io/docs/add-secure-apps/flows-stages/stages/user_login/

## LDAP Source

Fürs Einbinden vom Active Directory gibt es eine eigene Anleitung:

- https://docs.goauthentik.io/docs/users-sources/sources/directory-sync/active-directory/

## Troubleshooting
### Tokens
To see the tokens saved on the location machine, go in your browser to `Dev Tools > Application > Cookies`.

