VERSION 0.8

# convert a single file wiki to md by filename (without extension) e.g. --FILENAME index
wiki-to-md:
    ARG FILENAME
    FROM pandoc/core
    COPY *.wiki ./tmp/
    WORKDIR ./tmp
    RUN pandoc --from vimwiki --to markdown $FILENAME.wiki -o $FILENAME.md
    SAVE ARTIFACT $FILENAME.md AS LOCAL ./md/$FILENAME.md

# convert all wiki files to md
all-wiki-to-md:
    FROM pandoc/core
    COPY *.wiki ./tmp/
    # COPY +generate-public-index/public_index.wiki ./tmp/index.wiki
    RUN mkdir -p ./md
    RUN find ./tmp -name "*.wiki" -exec sh -c 'pandoc --from vimwiki --to markdown "$1" -o "./md/$(basename "$1" .wiki).md"' _ {} \;
    SAVE ARTIFACT ./md AS LOCAL ./md

pandoc-md-to-html:
    FROM pandoc/core
    ARG source
    COPY $source/* ./tmp/
    RUN mkdir -p ./html
    RUN find ./tmp -name "*.md" -exec sh -c 'pandoc --from markdown --to html "$1" -o "./html/$(basename "$1" .md).html"' _ {} \;
    RUN ls html
    SAVE ARTIFACT ./html AS LOCAL ./html

hugo:
    FROM ubuntu:latest
    # Hugo cannot work in /
    WORKDIR tmp
    ARG source
    COPY $source ./content
    COPY hugo.toml .
    RUN apt-get update -y && \
        apt-get install hugo git -y
    # RUN mkdir -p themes && \
    #     git clone https://github.com/1bl4z3r/hermit-V2 themes/hermit-v2
    # RUN echo 'themes = "hermit-v2"' >> hugo.toml
    RUN hugo version
    RUN hugo --config hugo.toml --themesDir ./themes
    SAVE ARTIFACT ./public AS LOCAL ./public

build:
    BUILD +hugo --source ./content
