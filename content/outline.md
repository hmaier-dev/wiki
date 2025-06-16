---
title: Outline
description: Collaborative wiki using React and Node.js
---

## Install
The recommended way to run Outline is through a `docker-compose.yml`. You can find the docu here: https://docs.getoutline.com/s/hosting/doc/docker-7pfeLP5a8t

Outline utilizes a postgres-database. Before the first start it needs to get initalized:
```bash
## Creation
docker compose run --rm outline yarn db:create --env=production-ssl-disabled
## Migration
docker compose run --rm outline yarn db:migrate --env=production-ssl-disabled
```
Run both commands in order.

When creating the database, this error can appear:
```bash
Sequelize CLI [Node: 20.19.1, CLI: 6.6.2, ORM: 6.37.3]

Loaded configuration file "server/config/database.json".
Using environment "production-ssl-disabled".

ERROR: getaddrinfo ENOTFOUND postgres

error Command failed with exit code 1.
info Visit https://yarnpkg.com/en/docs/cli/run for documentation about this command.
```
The outline container cannot find the postgres-container. To fix that explicitly create a network and put **all services** in it.

```yaml
networks:
  outline-net:
    name: outline-net
    driver: bridge

services:
  outline:
    networks:
      - outline-net
  postgres:
    container_name: postgres-outline  # fixed hostname
    networks:
      - outline-net
```
Also make sure to give the containers fixed names, so the variable in `docker.env` are right.

```bash
## docker.env
DATABASE_URL=postgres://user:pass@postgres-outline:5432/outline
```

## Integration with Outline

Reference:
- https://docs.goauthentik.io/integrations/services/outline/
