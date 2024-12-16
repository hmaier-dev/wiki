---
title: bash
---

#  Nützliche Kommandos

  Kommando                                                     Erklärung                                                                  
  ------------------------------------------------------------ -------------------------------------------------------------------------- ------------------------------------------------------------------------------
  +set -o vi                                                   vim-like movement in der shell aktivieren                                  
  CTRL+R                                                       Suche in der History. Mit \<ESC\> beenden.                                 
  xdotool getactivewindow set_window \--name \"Hello World\"   Change current window-name to \"Hello World\" (works from within tmux!!)   
  find . -type f \\                                            entr -r go run ./cmd/web                                                   Führt Kommando erneut aus sobald sich ein Datei in einem Unterordner ändert.
                                                                                                                                          
## Colors and Effects in Terminal

- https://misc.flogisoft.com/bash/tip_colors_and_formatting

## Change the extension of all files in a directory

In this case all \*.wiki files are getting renamed to \*.md.

\`\`\`bash find . -name \"\*.wiki\" -type f -exec sh -c \'mv
$(basename $`<!-- -->`{=html}1 .wiki).wiki
$(basename $`<!-- -->`{=html}1 .wiki).md\' \_ {} \\; \`\`\`

