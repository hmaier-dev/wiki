---
categories:
- editors 
title: Neovim
---

Is a fork from the original vim-project. Some key-features are:

- LSP-Integration
- Configuration with `lua`

## Vimscript essentials

The most fundamental config without lua.

```vim
filetype plugin indent on

set expandtab
set tabstop=2
set softtabstop=2
set shiftwidth=2

" Indentation and re-selection
vnoremap > >gv
vnoremap < <gv
```

## Keybindings Cheat Sheet

These just work with my setup, which is not public (right now).

- `<space>e` = vim.diagnostic.open_float
- `gd` = Go to definition
- `K` = Show docs for this symbol
- `<space>ff` = telescope.builtin.find_files
- `<space>fg` = telescope.builtin.live_grep
- `<space>fb` = telescope.builtin.buffers
- `<space>of` = telescope.builtin.oldfiles
- `<S>v`+ `<space>/` = comment out line/block

## Syntax-Highlighting

By default neovim has native syntax highlighting which cannot take it up with [Treesitter](https://tree-sitter.github.io/tree-sitter/).
When Treesitter is setup, you can install treesitter-parsers with the following command.

```lua
:TSInstall <tab>
```

By pressing <TAB> the autocompletion shows you a plethora of
installable languages.

With the `:InspectTree` you can display the the AST
(Abstract-Syntax-Tree) in a speperate window.

### Treesitter-Install

Beforehand you need to have Treesitter setup by your package-manager (in this case lazy.nvim):

```lua
return
  {
    {
      "nvim-treesitter/nvim-treesitter",
      build = ":TSUpdate",
      config = function()
        require("nvim-treesitter.configs").setup(
        {
          ensure_installed = { "lua", "vim", "go", "python", "bash" },
          auto_install = true,
          highlight = {
            enable = true,
          },
          ignore_install = { "ruby" },
        }) end,
    },
  }
```

## How to rename a variable?

There are several cases where you would want to
rename a variable. The place before the `s` is reserved for the scope,
which is:

- `'<,'>` currently selected
- `%` entire file

Go to the string of your choice and press `*`. All matched occurences
will be highlighted. Then do

```cmd
:%s/
```

With `C-r` you can paste the highlighted string. At first it looks like
this

```vim
:%s/"
```

After a `/`:

```vim
:%s/\<string\>
```

Continue with another `/` and your wanted string.

```cmd
:%s/\<string\>/mynewstring/
```

You can now specifiy, if you want to change globally with `g` (don\'t
know what this means) and if you want confirmation with `c`.

```cmd
:%s/\<string\>/mynewstring/gc
```

### Renaming a variable with LSP

If you have lsp configured, you can do it with `vim.lsp.buf.rename`:

```lua
-- Source: https://github.com/neovim/nvim-lspconfig?tab=readme-ov-file#suggested-configuration
-- Keymaps for LSP
v.keymap.set("n", "<space>e", v.diagnostic.open_float)
v.api.nvim_create_autocmd("LspAttach", {
 group = v.api.nvim_create_augroup("UserLspConfig", {}),
 callback = function(ev)
  local opts = { buffer = ev.buf }
  v.keymap.set("n", "<space>rn", v.lsp.buf.rename, opts)
 end,
})
```

### Renaming a variable in your entire project

The native vim-way goes like that:

```vim
:grep <string> `<location>`
:grep h.maier `find . -type f`
```

The seconds command would search all subdirectorys for `h.maier`.
Depending on the size of your project, this could take a while. You can
always abort the `grep` with `C-c`. After finishing the search, you can
load the found occurences into a *quickfix list* by doing a `:copen`.

If you use Telescope for searching
(which is way more ergonimic than the grep-method) you can use `C-q` to
load the found-occurences into a quickfix list.

From there on, `:cdo` is your friend. Replacing a variable-name goes
like this:

```vim
:cdo %s/h.maier/nobody/gc
```

`:cdo` lets you iterate through the quickfix list and execute the given
command for every entry.

## Adding characters to the END of every line of selected text

- select the block of text with `SHIFT + V`
- enter command mode with `:` (colon)
- at first it will look like this

``` cmd
:'<,'>
```

- go into normal mode with `norm` and write your commands

```vim
:'<,'>norm A <the-string-of-my-choice>
```

## Add at the end of every line

```cmd
:%norm A<stuff-that-you-want-to-add>
```

Which means:

- \% = for every line
- norm = type the following commands
- A\* = append \' \* \' to the end of current line

## How to enter the commandline history?

Just press `q:` (not `:q`). Now you can browse through are executed commands and copy them.

## Plugins

The plugin manager of my choice is `lazy.nvim`. Have a look at
[lazy.folke.io](https://lazy.folke.io/) to get to know how its done.

## Lua

Ein angenehmes Tool um den ganzen Lua-Code nach nem Herumfuschen
übersichtlicher zu machen ist `stylua`. Mehr zu Lua gibt es hier:
[lua](lua)

## Neovim in the Browser

- https://github.com/coder/code-server

## Troubleshooting

### Fehler nach Updates von Plugins

In einer Vielzahl von Fällen treten Probleme nach Updates von Plugins
auf. Lässt sich der Fehler nicht zur eigenen Konfiguration, sondern in
den Quellcode des Plugin zurückverfolgen, ist es am einfachsten das
Plugin einfach neu zu installieren.

Dies funktioniert unter `Lazy.nvim` in dem
man das geklonte Repository unter `~/.local/share/nvim/lazy/<repo>` löscht.
