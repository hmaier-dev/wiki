VERSION 0.8
FROM hmaierdev/hugo-plus-tailwind

build:
    # workdir is /tmp
    # Hugo cannot work in root (/)
    COPY --dir content assets layouts ./
    COPY hugo.toml hugo.toml
    COPY tailwind.config.js tailwind.config.js

    # generate meta-data
    COPY build/count-lines.sh .
    RUN ./count-lines.sh

    RUN hugo
    RUN ls -la public
    SAVE ARTIFACT ./public AS LOCAL ./public
