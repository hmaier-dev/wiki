---
categories:
- cli
title: bash
---

## TL;DR

- How to lock a account: `usermod -L user` (unlock it with `-U`)

##  Nützliche Kommandos

- `+set -o vi`: vim-like movement in der aktivieren 
- `CTRL+R`: Suche in der History. Mit `<ESC>` beenden.
- `find . -type f | entr -r go run ./cmd/web`: Führt Kommando erneut aus sobald sich ein Datei in einem Unterordner ändert.
                                                                                                                                          
## Colors and Effects in Terminal

- https://misc.flogisoft.com/bash/tip_colors_and_formatting

## if-else
If you want to test a string, you can use

- `-n` to test if var *is not empty*
- `-z` to test if var *is empty*

## xargs
Search for string in file list comming from a pipe.
```bash
dfr ls-files | xargs grep "my searched string"
```
`xargs` execute the following command on all received files.
