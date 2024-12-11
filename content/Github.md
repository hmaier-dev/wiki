# How this wiki works

The wiki files are stored in my private dotfiles repository.
Since I prefer to keep this repository private, but GitHub Pages requires a public repository, I push the necessary files to a separate public repository for publishing.

### 1. Committing Changes to the Private Repository
Any changes made in docs/vimwiki are committed and pushed to the private remote repository.


### 2. Syncing to the Public Repository
A GitHub Actions workflow automates the process of syncing changes to the public repository. Here's how it works:
    - The workflow clones the public wiki repository.
    - It updates the specified files based on a whitelist.
    - Finally, it commits and pushes the changes back to the public repository.
    
#### Access Token Setup
To enable this process, you need a GitHub personal access token with repo permissions. You can generate one at [GitHub Settings > Tokens](https://github.com/settings/tokens). When cloning the public repository, the token is passed as part of the URL, like this:
```
            git clone --single-branch --branch main \
              "https://x-access-token:$TOKEN@github.com/user/public-repo.git" "repo"
```

### 3. Publishing via Hugo
When the changes arrive in the public-repository `.github/workflows/publish.yml` converts the markdown to html via Hugo.
    - The complete logic for the markdown-to-html-conversion is written inside an `Earthfile` which is part of Eahrtly. That\'s because, with Earthly you can debug/test your CI-Pipeline locally. This way you do not need to push you changes to Github and wait for the Runner.
