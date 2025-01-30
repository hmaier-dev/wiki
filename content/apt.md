---
categories:
- linux
title: apt
---

The **Advanced Packaging Tool** is a frontend for `dpkg` and is mostly used on debian-based distros.

## Unsupported architectures 

Viele Paket-Repos supporten nicht alle existierenden Architekutren:

```bash
N: Skipping acquire of configured file 'main/binary-i386/Packages' as repository 'http://dl.google.com/linux/chrome/deb stable InRelease' doesn't support architecture 'i386'
```
Diese Warnung kann man umgehen, wenn man die Architekture festzurrt:
```bash
deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main
```

Bei mehreren Variablen in den Brackets, einfach durch ein Leerzeichen
trennen.

Source: https://askubuntu.com/questions/741410/skipping-acquire-of-configured-file-main-binary-i386-packages-as-repository-x

## Information über Paket 

Dabei ist `apt-cache` dein Freund.
