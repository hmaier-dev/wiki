VERSION 0.8

pandoc:
    FROM pandoc/core
    ARG source
    COPY $source/* ./tmp/
    RUN mkdir -p ./public
    # Markdown to Html
    RUN find ./tmp -name "*.md" -exec sh -c 'pandoc --from markdown --to html "$1" -o "./public/$(basename "$1" .md).html"' _ {} \;
    SAVE ARTIFACT ./public AS LOCAL ./public

hugo:
    FROM ubuntu:latest
    # Hugo cannot work in root (/)
    WORKDIR tmp
    COPY ./content ./content
    COPY hugo.toml .
    RUN apt-get update -y && \
        apt-get install hugo git -y > /dev/null
    RUN mv ./content/index.md ./content/_index.md
    RUN mkdir -p themes && \
        git clone https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
    RUN echo 'themes = "ananke"' >> hugo.toml
    RUN hugo --config hugo.toml --themesDir ./themes --contentDir ./content
    RUN ls -la ./public
    SAVE ARTIFACT ./public AS LOCAL ./public

build:
    # BUILD +hugo --source ./content
    BUILD +pandoc --source ./content
