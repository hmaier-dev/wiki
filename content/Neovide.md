---
categories:
- Windows
- editors
title: Neovide
description: A neovim-gui written in rust.
---

This is written in rust (important!) and can do pretty graphical things.

## Font
When opening up Neovide at first, the font might be a little to big. You can change this in your `init.lua` by adjusting `h12`-part.
```lua
if v.g.neovide then
  v.o.guifont = "CaskaydiaCove Nerd Font:h12"
end
```
The used font can be downloaded here: https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/CascadiaCode.zip
