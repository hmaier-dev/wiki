---
categories:
- cli
- linux
title: tmux
---

Is a terminal multiplexer which nullified my need for a tiling window manager.

## Move pane to new window 

```sh
CTRL+b; !
```

## Resize pane in tty 
You need to remap the keys, because tty isn't very advanced.
https://superuser.com/questions/688807/how-to-resize-tmux-panes-inside-tty

## New Session
From within tmux you can use `new -s` in the tmux cli.
```bash
CTRL+b; 
:;
new -s mynewsession
```
## New base directory
From within tmux you can use `attach-session -c` in the tmux cli.
```bash
CTRL+b; 
:;
attach-session -c ~/.config/nvim
```
## Rename tab
Renames the current tab
```bash
CTRL+b; 
,
```
