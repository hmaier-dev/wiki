VERSION 0.8

FROM ubuntu:latest

generate-public-index:
    FROM python:3.10
    COPY index.wiki .
    COPY src/extract.py .
    RUN python extract.py index.wiki public_wiki.wiki
    SAVE ARTIFACT public_index.wiki AS LOCAL ./index.wiki
