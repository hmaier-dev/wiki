---
categories:
- CI/CD
title: Gitlab
---

## Include a foreign job

```yaml
include:
  - remote: https://gitlab.com/repo/dir/-/raw/version/jobs.yml

stages:
  - test
  - deploy
  - apply

test:
  stage: test
  extends: [.gj_earthly]
  script:
    - earthly --no-output +test
  only:
    - branches
  except:
    - production
```

-   extends: Inherits this job (could be keept in a seperate file and
    imported)
    -   e.g.: `gj_earthly` is keept in a different repo in the
        `jobs.yml` which is imported at the top
-   only/except: <https://docs.gitlab.com/ee/ci/yaml/#only--except>

Basic Syntax: <https://docs.gitlab.com/ee/ci/yaml/>
