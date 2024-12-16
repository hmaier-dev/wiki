---
title: Docker
---


# Docker 

## TL;DR

-   Alle Container; both running & stopped:
    -   `docker ps -a`
-   Alle Container die gerade laufen:
    -   `docker ps`
-   IP-Adresses aller Container:
    -   `docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q)`
-   Shell in Container öffnen
    -   `docker exec -it <container_id_or_name> /bin/bash`
-   Directory in Container mounten:
    -   `docker run -v <absolute-local-path>:<path-inside-container> <image>`
-   Einzelnen Container aus `docker-compose`-File neustarten
    -   `docker compose up --no-deps <service-name>`
-   Herausfinden was sich in einem Volume alles befindet:
    -   ` docker run -it -v deploy-wordpress_wordpress:/mnt ubuntu /bin/bash`

## `docker inspect`

Um Mehr Über das Image zu erfahren kann man mit

``` bash
docker inspect <image:version>
```

jegliche Daten ausgegeben kriegen, die von vom Ersteller:in eingegeben
wurden.

## Entrypoint

Möchte man das vorgegebene Verhalten, beim Starten des Containers,
ändern, kann man den `--entrypoint` überschreiben. Dies kann hilfreich
sein, wenn man sich bspw. nur das *innere* des Containers anschauen
möchte ohne das irgendetwas gestartet wird.

Überschreiben mit der Bash-Shell würde wie folgt funktionieren:

``` bash
docker run \
    --entrypoint /bin/bash \
    -it \
    <image:version>
```

Das `-it` ist nötig, um ein `Exit(0)` des Containers zu verhindern.
`Exit(0)` würde passieren, wenn die Shell merkt, dass sich niemand
verbindet.
