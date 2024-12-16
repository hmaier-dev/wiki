---
title: Postgres
---

# Postgres 

## Nützliche Kommandos 

-   Get all databases:
    -   `\l`
-   Connect to or better, use a database:
    -   `\c <db_name>`
-   Connect to db from shell:
    -   `psql -h 172.17.0.2 -U postgres`
-   Import data into database:
    -   `psql -h 172.17.0.3 -U postgres  cmdb < ~/cmdb.sql`
-   Adminer in Docker starten, um Frontend für die Datenbank zu haben:
    -   `docker run --name adminer --link cmdb -p 8080:8080 adminer`
-   Datenbank mit Docker aufsetzen:
    -   `docker create --name cmdb -e POSTGRES_PASSWORD=password postgres:15`
-   Postgres-URL:
    -   `url="postgres://postgres:password@172.17.0.3/cmdb"`
