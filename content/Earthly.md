---
title: Earthly
---

# Earthly 

Ist ein Buildtool welches Container nutzt, um die Toolchain bereit
zustellen. Verschiedene Targets werden über ein sogennates `Earthfile`
deklariert. Erinnern tut `earthly` dabei, an klassiche Makefiles.

Der große Vorteil an `earthly` ist die Portabilität. Man kann seine
CI-Pipeline lokal zusammenbauen und erhält bei Runs enau die gleichen
Ergebnisse wie im Gitlab.

Ein einziges Target, welches Python-Skripte auf ihre Richtigkeit testet,
kann beispielsweise so aussehen:

``` Dockerfile
syntax-python:
    FROM python:3.12.3 # pullt python-image
    WORKDIR /src
    COPY --dir my/project/path container/path
    COPY some/other/dir/*.py container/path

    RUN find ./path -name "*.py" | xargs -t -P4 -n1 python3 -m py_compile
```

Zusammen mit anderen Targets, kann dieses verkettet werden.

``` Dockerfile
test-all:
    BUILD +syntax-go
    BUILD +syntax-python
    BUILD +syntax-bash
    BUILD +test-database
```

# `SAVE ARTIFACT LOCALLY`

Dieses Kommando wird nur Dateien ins Host-Filesystem ausgeben, wenn die
`--ci`-Flag nicht mitgegeben wurde (`--help` um zu erfahren was sie
impliziert).

<<<<<<< HEAD
=======
# `SAVE ARTIFACT`

Möchte man Artifacts aus einem anderen Target importieren, kann man das wie folgt tun.
```Dockerfile
target:
  COPY +download-hugo/<articfact> /path/to/copy/to
  
  COPY +download-hugo/hugo /usr/local/bin/hugo
  COPY +download-tailwindcss/tailwindcss /usr/local/bin/tailwindcss
```
  
# `.secrets`
For deploying from your local machine, you need your secrets present in a `.secrets` file. That must be located in the same directory as the `Earthfile`.
For multi-line secrets use `''` like in the following example:
```
host=192.168.13.12
port=1337
username=secret-username
key='-----BEGIN OPENSSH PRIVATE KEY-----
SOMEVALIDCHARACTERSWHICHMAKEUP
AVERYGOODSECRETANDSAFEPRIVATEK
-----END OPENSSH PRIVATE KEY-----'
known_hosts='content-of-the-known-hosts-file'
```
The `''` are needed because they keep the format (like newlines etc).

>>>>>>> 79e1b6bee0a65e3e5eae7f3cb7d8383d5a97205b
# Errors
## Error: could not determine buildkit address - is Docker or Podman running?
If you encounter this error, first look if the systemd-service is running.
```bash
systemctl status docker.service
```
If it is, you/Earthly probably don't have sufficient rights to call docker. You can test this, by manually calling docker without sudo/doas.

```bash
docker ps -a
# Output:
# permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock:
# Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.46/containers/json?all=1": 
# dial unix /var/run/docker.sock: connect: permission denied
```
The solution to this problem, is to add your user-group to the docker group.
```bash
sudo usermod -aG docker <username>
```

## `failed to stat parent: stat /tmp/earthly/buildkit/runc-overlayfs/snapshots/snapshots/2006/fs: no such file or directory`

Something with the cache was wrong. I resolved the issue with: `earthly prune -a` which cleared the cache.

More on how to manage the cache:

- https://docs.earthly.dev/docs/caching/managing-cache

