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

# `SAVE ARTIFACT` 

Dieses Kommando wird nur Dateien ins Host-Filesystem ausgeben, wenn die
`--ci`-Flag nicht mitgegeben wurde (`--help` um zu erfahren was sie
impliziert).

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
