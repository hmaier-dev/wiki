---
title: Hugo
---

# Hugo
Is a generator for static html. 

## Develop locally with Hugo

If you already have the needed directory structure and you'd want to know how the website will
look, just use 
```bash
hugo server
```
and `hugo` will provide a local webserver for you. 

Make sure to change the `baseURL`:
```toml
# baseURL = "https://hmaier-dev.github.io/wiki/"
baseURL = "http://localhost:1313/wiki"
```

Otherwise the local `css` won't load correctly.

If you ever change something under the `layouts`-directory, make sure to `earthly +build` the whole thing.

At last make sure to `git restore hugo.toml`!

## Config-file

Hugo needs config-file, which default is `hugo.toml`.
```toml
baseURL = "https://hmaier-dev.github.io/wiki/"
languageCode = "de-us"
title = "Wiki"
```

## Configuration
You will need several things for Hugo.

- a `./content`-directory with your knowlegde written in markdown (`.md`)
- some layout files under `./layouts/_default`, so Hugo knows how to structure the site
- and a config file, which can be `toml`, `json` or something else 
  
Default directory structure looks like this
```bash

├── content
│   ├── _index.md
│   └── some-page.md
├── hugo.toml
├── layouts
│   ├── _default
│   │   ├── baseof.html
│   │   ├── index.html
│   │   └── single.html
│   └── partials
│       ├── footer.html
│       ├── header.html
│       └── head.html
└── static
    └── css

```

## Layouts
There is a lookup-routine over which Hugo iterates. If it finds no Theme or other layouts, it will use the files in `./layouts/_default/`.
For example, these files could look like this.

- `baseof.html`
``` html
<!DOCTYPE html>
<html lang="{{ or site.Language.LanguageCode }}" dir="{{ or site.Language.LanguageDirection `ltr` }}">
<body>
  <main>
    {{ block "main" . }}{{ end }}
  </main>
</body>
</html>
```
- `index.html`: uses `_index.md` to generate the landing page (the underscores is mandatory)

``` html
{{ define "main" }}
    {{.Content}}
{{ end }}
```
- `single.html`: defines how a normal page (like `some-page.md`) would look

``` html
{{ define "main" }}
    {{.Content}}
{{ end }}
```
In this example, there is no logic at all. Therefore your markdown gets converted in the most basic way.

## Templating System
If you have worked with the Golang-modules `html/template` or `text/template`, this should look familiar to you.
Indeed you can use native Golang-functions, like `printf` or `date`. Also there is Metadata like `.RelPermalink` or `.Title` which is provided by Hugo.
Use both docs for problem solving:

- https://gohugo.io/quick-reference/
- https://pkg.go.dev/text/template

For more examples, just look at:

- https://themes.gohugo.io/

### Examples

#### Adding a variable to the `REPLACEMENT` when using `replaceRE`
At first I glance it tried to manually insert the variable `$Link` (which is `.RelPermalink`) into the `REPLACEMENT`.
```html
{{  with .Content  }}
{{ $Link := .RelPermalink }}
{{ . | replaceRE "(<h[1-9] id=\"([^\"]+)\".+)(</h[1-9]+>)" `${1}<a href="$Link#${2}" class="hanchor" ariaLabel="Anchor">#</a> ${3}` | safeHTML }}
{{  end  }}
```
Doing it this way, the variable just won't get display. Turns out I can use `printf` to alter the string before `replaceRE` does it jobs.
```html
{{  with .Content  }}
    {{ $Link := $.RelPermalink }}
    {{ . | replaceRE "(<h[1-9] id=\"([^\"]+)\".+)(</h[1-9]+>)" (printf `${1}<a href="%s#${2}" class="hanchor" ariaLabel="Anchor">#</a> ${3}` $Link)  | safeHTML }}
{{  end  }}
```

## Menus

In Hugo navbars are called menus.

- Offical docs: https://gohugo.io/content-management/menus/
- Helpful article: https://harrycresswell.com/writing/menus-in-hugo/



