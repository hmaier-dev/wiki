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
