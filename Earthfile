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
    FROM alpine:3.20
    RUN apk add --no-cache hugo

    # Hugo cannot work in root (/)
    WORKDIR tmp
    COPY content content
    COPY static static
    COPY hugo.toml hugo.toml
    COPY layouts layouts

    # generate meta-data
    COPY build/count-lines.sh .
    RUN ./count-lines.sh

    RUN mv content/index.md content/_index.md
    RUN hugo
    RUN ls -la public
    SAVE ARTIFACT ./public AS LOCAL ./public

build:
    BUILD +hugo --source ./content
    # BUILD +pandoc --source ./content
