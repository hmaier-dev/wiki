---
categories:
- cli
title: gh
description: use git over https.
---
If port 22 isn't available in your network and you cannot use key-pairs to authenticate to github. You can use the internal github-tool `gh`, which uses https.

## multiple accounts

- https://github.blog/changelog/2023-12-18-log-in-to-multiple-github-accounts-with-the-cli/

## switch accounts
```bash
gh auth status
```

## repo not found
Can happen if switch accounts. Re-auth with this command:
```
gh auth refresh -h github.com -s repo
```
