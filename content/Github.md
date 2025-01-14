---
title: Github
---

# How this wiki works

The wiki files are stored in my private dotfiles repository.
Since I prefer to keep this repository private, but GitHub Pages requires a public repository, I push the necessary files to a separate public repository for publishing.

### 1. Committing Changes to the Private Repository
Any changes made in `docs/vimwiki` are committed and pushed to the private remote repository.


### 2. Syncing to the Public Repository
A GitHub Actions workflow automates the process of syncing changes to the public repository. Here's how it works:

- The workflow clones the public wiki repository.
 
- It updates the specified files based on a whitelist.
 
- Finally, it commits and pushes the changes back to the public repository.

The workflow located in `~/.github/workflow/wiki.yml` looks like this:

```yaml

name: Update all wiki articles

on:
  push:
    branches:
      - main
    paths:
      - docs/vimwiki/**

jobs:
  publish:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./docs/vimwiki
    env:
      content: ./wiki/content
    steps:
      - uses: actions/checkout@v4
      - name: Cloning repo
        env:
          # Github personal access token 
          TOKEN: ${{ secrets.WIKI_REPO_TOKEN_RW }}
        run: |
            git config --global user.email "<>"
            git config --global user.name "Github Actions Runner"
            git clone --single-branch --branch main \
              "https://x-access-token:$TOKEN@github.com/hmaier-dev/wiki.git" "wiki"
      - name: Removing old files
        run: |
            find  $content -name '*.md' -type f -exec rm {} \;
            ls -la
      - name: Copy over new files
        run: |
            # Whitelist of all publishable wiki articles
            cp index.md $content
      - name: Setup Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.12'
          
      # Optional:  
      # Give special treatment to index.wiki because it needs to get censored
      - name: Censor index.wiki
        run: |
          cd $content
          python ../build/extract.py index.md
          
      # Pushing to the public wiki
      - name: Commit and push new files
        run: |
            cd wiki
            git checkout main
            git add .
            git diff-index --quiet HEAD || git commit -m "Automatic wiki-publish"
            git push origin main

```
    
#### Access Token Setup

To enable this process, you need a GitHub personal access token with repo permissions. You can generate one at [GitHub Settings > Tokens](https://github.com/settings/tokens). When cloning the public repository, the token is passed as part of the URL, like this:
```
            git clone --single-branch --branch main \
              "https://x-access-token:$TOKEN@github.com/user/public-repo.git" "repo"
```

### 3. Publishing via Hugo
When the changes arrive in the public-repository, the `publish.yml` workflow is triggered.
Running the workflow sets up `earthly` and uses it running hugo and publishes the generated html to the github-pages.

#### Earthly
Earthly is like a Makefile for CI. All logic is declared in the `Earthfile`. This file enables me to declare different targets, which every of them spawns a docker-container.
By using Earthly I can run my CI locally without waiting for a runner.

```
VERSION 0.8

hugo:
    FROM alpine:3.20
    RUN apk add --no-cache hugo

    # Hugo cannot work in root (/)
    WORKDIR tmp
    COPY content content
    COPY static static
    COPY hugo.toml hugo.toml
    COPY layouts layouts

    RUN mv content/index.md content/_index.md
    RUN hugo
    RUN ls -la public
    SAVE ARTIFACT ./public AS LOCAL ./public

build:
    BUILD +hugo
```
The generated html-files are getting exporter to `./public`, which is the `publish_dir` for Github-Pages.


# Actions

## Setting up ssh access for runner to vm

You will need create a key-pair. On the runner you will need the private key and on the vm the public key.

- `id_rsa` goes into e.g. `{{ secrets.SSH_KEY }}`
- `id_rsa.pub` goes into ~/.ssh/authorized_keys on the vm

Best practice would be to create the user on your local machine and distribute the keys from there.

```bash
useradd deploy
passwd deploy
su deploy
ssh-keygen -t ed25519 -a 200 -C "runner@github.com"
ls -la  ~/.ssh
```
## Updating static html on vm
When ssh is setup right, you can over the files with `rsync`.
```bash
rsync -rav ./public deploy@vm:~/<dir-for-html>
```
The deploying user (e.g. `deploy`) must be in the same group as nginx user (e.g. Group: `www-data`). You achieve this by:
```bash
usermod -a -G www-data deploy
```
To ensure all files have the right ownership, set the `setgid`-bit on the `<dir-for-html>.
```bash
chmod -R g+s <dir-for-html>
```

# Secrets

When passing multi-line secrets, make sure to border the secret with `"` like this:
```bash
earthly --secret host=${{ secrets.SSH_HOST }} \
--secret username=${{ secrets.SSH_USER }} \
--secret key="${{ secrets.SSH_KEY }}" \
+deploy-test
```
The `"` keeps the format in it's right place.
