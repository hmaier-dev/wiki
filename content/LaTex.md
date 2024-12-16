---
title: LaTex
---

# LaTex

## How to pass variables to LaTex?

If you have a markdown-document and you have e.g. $fontsize$
in you documentclass, you can pass the variable into the YAML-header
of the markdown-document.

This is the LaTex:
```latex
\documentclass[
$fontsize$,
$for(classoption)$
  $classoption$$sep$,
$endfor$
]{scrlttr2}

```
And the markdown will look like this:

```markdown
---
fontsize: 12pt
classoption: enlargefirstpage,firstfoot=false
---
The actual text starts here...

```
