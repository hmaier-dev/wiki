---
categories:
- cli
- linux
title: ssh
description: tips about using Secure Shell.
---

## TL;DR

- Where to find the ssh access logs?
    - Under `/var/log/auth.log`
    - With `sudo journalctl -t sshd -n 100`

## Basic config

```txt
Host <name-you-want-to-type>
    HostName <ip>
    User <user>
```

