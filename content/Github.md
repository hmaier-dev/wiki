# How this wiki works

The wiki-files are stored inside my dotfiles repository. Because reasons
I don\'t want to have my dotfiles repo public, but for Github-Pages it
needs to be. So I\'m pushing the wanted files to my public repos, where
I publish them.


1. Changes in `docs/vimwiki` getting committed/pushed to the private-remote-repository
2. Workflow `.github/workflows/wiki.yml` clones the public-wiki-repository, updates all registered files (whitelist) and committes/pushes the changes. 
    - For this you need a access token, which you can generate at https://github.com/settings/tokens. Fill out the repo-permissions.
    - The token will passed in when cloning the public-repository. It could look like this:
```
            git clone --single-branch --branch main \
              "https://x-access-token:$TOKEN@github.com/user/public-repo.git" "repo"
```
3. When the changes arrive in the public-repository `.github/workflows/publish.yml` converts the markdown to html via Hugo.
    - The complete logic for the markdown-to-html-conversion is written inside an `Earthfile` which is part of Eahrtly. That\'s because, with Earthly you can debug/test your CI-Pipeline locally. This way you do not need to push you changes to Github and wait for the Runner.
