VERSION 0.8

# removes links (in index.wiki) for articles, which have not been copied
generate-public-index:
    FROM python:3.12
    COPY index.wiki ./tmp/
    COPY *.wiki ./tmp/
    COPY build/extract.py ./tmp/
    WORKDIR ./tmp
    RUN python extract.py index.wiki public_index.wiki
    SAVE ARTIFACT public_index.wiki AS LOCAL ./index.wiki

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
    RUN mkdir -p ./md
    RUN find ./tmp -name "*.wiki" -exec sh -c 'pandoc --from vimwiki --to markdown "$1" -o "./md/$(basename "$1" .wiki).md"' _ {} \;
    RUN ls -la
    SAVE ARTIFACT ./md AS LOCAL ./md


              




