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