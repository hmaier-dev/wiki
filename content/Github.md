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
            # Example for acces token found at: https://github.com/dmnemec/copy_file_to_another_repo_action/blob/main/entrypoint.sh#L28
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
            # more publishable markdown files...
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
When the changes arrive in the public-repository `.github/workflows/publish.yml` converts the markdown to html via Hugo.

### Why Earthly?
Earthly allows you to debug and test the CI pipeline locally. This eliminates the need to push changes to GitHub and wait for the Runner, significantly speeding up the development process.
