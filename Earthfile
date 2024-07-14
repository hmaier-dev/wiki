VERSION 0.8

FROM python:3.12

generate-public-index:
    COPY index.wiki ./tmp/
    COPY *.wiki ./tmp/
    COPY build/extract.py ./tmp/
    WORKDIR ./tmp
    RUN python extract.py index.wiki public_index.wiki
    SAVE ARTIFACT public_index.wiki AS LOCAL ./index.wiki
