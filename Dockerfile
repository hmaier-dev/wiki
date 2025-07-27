FROM debian:bullseye
LABEL org.opencontainers.image.source=https://github.com/hmaier-dev/wiki

WORKDIR /tmp
RUN apt-get update && apt-get install -y curl git bash && \
    curl -SLO https://github.com/gohugoio/hugo/releases/download/v0.140.2/hugo_0.140.2_linux-amd64.tar.gz && \
    tar -xvzf hugo_0.140.2_linux-amd64.tar.gz && \
    chmod +x hugo && \
    mv hugo /usr/local/bin/hugo && \
    curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v4.0.0-beta.8/tailwindcss-linux-x64 && \
    chmod +x tailwindcss-linux-x64 && \
    mv tailwindcss-linux-x64 /usr/local/bin/tailwindcss && \
    rm -rf /tmp/* && \
    apt-get remove -y curl
