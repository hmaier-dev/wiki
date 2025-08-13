---
categories:
- Container
title: Docker
description: Container engine. Run your application on different systems.
---


## TL;DR

- Dockerfile bauen:
  - `docker build --tag 'username/my-custom-name' .`
- Alle Container; both running & stopped:
    -   `docker ps -a`
- Alle Container die gerade laufen:
    -   `docker ps`
- IP-Adresses aller Container:
    -   `docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q)`
- Shell in Container öffnen
    -   `docker exec -it <container_id_or_name> /bin/bash`
- Directory in Container mounten:
    -   `docker run -v <absolute-local-path>:<path-inside-container> <image>`
- Einzelnen Container aus `docker-compose`-File neustarten
    -   `docker compose up --no-deps <service-name>`
- Herausfinden was sich in einem Volume alles befindet:
    -   ` docker run -it -v deploy-wordpress_wordpress:/mnt ubuntu /bin/bash`
- Alle Container inklusive Volumen löschen:
    - `docker rm -vf $(docker ps -aq)`
- Alle Images löschen
    - `docker rmi -f $(docker images -aq)`
- Wie lade ich ein Image in meine Docker-Registry?
    - Erst einloggen mit `docker login`.
    - Danach `docker push <username>/<image-name>:latest`
- Wie erstelle ich ein neues `:latest`-image?
  1. Retag the old image: `docker tag <image_id> my-tool:previous``
  2. Remove old latest tag: `docker rmi my-tool:latest`
  3. Build new image with latest: `docker build -t checklist-tool:latest .`

## Installation

Install via `apt`: https://docs.docker.com/engine/install/debian/#install-using-the-repository
Add user to Docker-Group: https://docs.docker.com/engine/install/linux-postinstall/

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

## Optimizing Image size
Anstatt viele `RUN`-Kommandos zu verwenden, die jedes Mal einen neuen Layer aufmachen, bietet es sich an ein einziges `RUN` mit dem `&&`-Operator zu nehmen.
Wenn du unschlüssige bist, warum der Container so riesige geworden ist, hilft ein
```bash
docker image history <img>
```
Damit wird die Größe der einzelnen Layer angezeigt.

## Github Container Registry
You need to give the `docker`-command the permissions to access the Github-Container-Registry (ghcr).
You do this via a *Personal access token*. Find the option for this under https://github.com/settings/tokens.
The token needs the following permissions:

- write:packages
- delete:packages

```bash
docker login ghcr.io -u <USER> --password <TOKEN>
docker build . -t ghcr.io/user/repo:v0.1
docker push ghcr.io/user/repo:v0.1
```

You can now pull the image with
```bash
docker pull ghcr.io/user/repo:v0.1
```
More on this topic: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry

## Troubleshooting

### Container stoppt langsam & gibt Exit Code 137
Die Binary die im Container läuft hat das `SIGKILL` nicht erhalten und Docker wartet eine vordefinierte Zeit lang bis er den Container runterfährt.
Dabei wird die Binary (bzw. das Programm) nicht ordentlich geschlossen. Die Binary erhält das `SIGKILL` nicht, da sie nicht `PID 1` ist.
Das kann vorkommen, wenn man das Programm mit einem `bash -c` oder über `CMD` startet.

Abhilfe schafft `ENTRYPOINT` im JSON-Format:
```bash
ENTRYPOINT ["./binary", "-db", "mysqlite.db"]
```
Ob die Binary `PID 1` ist, kann man testen in dem man im Container nachschaut (lol).
```
docker exec -it <container> ps aux
```
