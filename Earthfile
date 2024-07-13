VERSION 0.8
FROM ubuntu:latest


publish:
    RUN apt-get update && apt-get install -y git
    ARG REPO_URL=https://github.com/hmaier-dev/wiki.git
    ARG REPO=wiki
    ARG WIKI_REPO_TOKEN

    GIT CLONE $REPO_URL $REPO

    WORKDIR wiki

    RUN find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

    RUN echo "This is a whitelist of all publishable articles."
    COPY Ansible.wiki .
    COPY Arch.wiki .
    COPY Docker.wiki .
    COPY Earthfile .
    COPY Earthly.wiki .
    COPY Foreman.wiki .
    COPY Github.wiki .
    COPY Github.wiki  .
    COPY Gitlab.wiki .
    COPY Gnome.wiki .
    COPY Golang.wiki .
    COPY Goose.wiki .
    COPY Linux.wiki .
    COPY Neovim.wiki .
    COPY Postgres.wiki .
    COPY Puppet.wiki .
    COPY Python.wiki .
    COPY Raspberry_Pi.wiki .
    COPY Vagrant.wiki .
    COPY Windows.wiki .
    COPY Wordpress.wiki .
    COPY apt.wiki .
    COPY bash.wiki .
    COPY crane.wiki .
    COPY git.wiki .
    COPY htmx.wiki .
    COPY index.wiki .
    COPY lua.wiki .
    COPY pgTAP.wiki .
    COPY systemd.wiki .
    COPY tmux.wiki .
    COPY vim.wiki .

    RUN git tag -d main
    RUN git checkout main
    RUN git remote set-url origin https://hmaier-dev:$WIKI_REPO_TOKEN@github.com/hmaier-dev/wiki.git
    RUN git config --global user.email "hendrik_maier@protonmail.com" && \
        git config --global user.name "hmaier-dev"
    RUN git add *.wiki

    RUN --push git commit -m "wiki-update"
    RUN --push git push -u origin main
