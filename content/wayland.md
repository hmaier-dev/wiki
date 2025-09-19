---
title: Wayland
description: Communication protocol between the display server and its client. Often seen as modern alternative for Xorg on Linux.
---
Everything about wayland can be read in
- https://wayland-book.com/

## Application
### Brave-Browser
To use the brave browser on wayland, you need to add some flags.
```bash
## ~/.config/brave-flags.conf
--enable-features=UseOzonePlatform
--ozone-platform=wayland
```
After this brave should start flawless. (Tested on Brave Browser 139.1.81.137)

## Keyboard
Wayland uses xkb under the hood. There are several xkb programs (e.g. `xkbcli`) which can help you with problem solving.

## KeepassXC
Usually build with Qt-5. Using Qt-5 it needs the env-variable `QT_QPA_PLATFORM=wayland` to start.
Force it by setting it in the terminal:
```bash
QT_QPA_PLATFORM=wayland keepassxc
```
If you don't know wether your programm was build with Qt-5, you can check the linked library with `ldd`
```bash
ldd $(which keepassxc) | grep Q
```

