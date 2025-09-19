---
categories:
- Web-Development
title: Hugo
---

Is a generator for static html. 

## Develop locally with Hugo

If you already have the needed directory structure and you'd want to know how the website will
look, just use 
```bash
hugo server
```
and `hugo` will provide a local webserver for you. To open connections from your phone or another client in the local network use
`--bind`.
```bash
hugo server --bind 0.0.0.0 --baseURL http://<ip-of-you-device>:1313/wiki
```
You can use `--baseURL` to overwrite the `baseURL`, so that you don't have to change the `hugo.toml`.
When developing locally you need to do either, because otherwise the `css` won't load and links won't direct correctly.

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

### Adding a variable to the `REPLACEMENT` when using `replaceRE`
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

> [!TIP]
> By the way: You can do **Anchors** also this way: https://gohugo.io/render-hooks/headings/#examples
> But beware, you cannot use `.RelPermalink` when doing this.


## Menus
In Hugo navbars are called menus.

- Offical docs: https://gohugo.io/content-management/menus/
- Helpful article: https://harrycresswell.com/writing/menus-in-hugo/

### Nav with all regular pages
Regular pages are the ones, that you added. With `site.AllPages` you would receive more.
This snippet would be located in `layouts/partials/nav.html`.
```html

<nav>
{{ range site.RegularPages }}
    <ul>
        <a href="{{ .RelPermalink }}">{{ .LinkTitle }}</a>
    </ul>
{{ end }}
</nav>
```

## Shortcodes
Shortcodes are functions for custom html. You can embbed them into your markdown content or into your layouts.
If you have some arguments like a changing `src=` or a different `id=` can use a shortcode. Shortcodes cannot be used in `layouts`.
Use them inside your markdown `content`.

Here are some example, made by the hugo-team:

- https://github.com/gohugoio/hugo/tree/master/tpl/tplimpl/embedded/templates/shortcodes
- Docs: https://gohugo.io/templates/shortcode/#create-custom-shortcodes

## Syntax Highlighting

Hugo uses Chroma for syntax highlighting. Here is the link to the docs: https://gohugo.io/content-management/syntax-highlighting/

## Ressources
When trying to access a ressource this way, you need to have a `assets`-directory containing `css/main.css`. It won't work with a `static`-directory.
```go
{{ $css :=  resources.Get "css/main.css" }}
```

## TailwindCSS
By `resources.Get` you can pass the content to `css.TailwindCSS` which outputs into `public/css/<name>.css`. This is elegant because of two reasons:

- `hugo server` triggers a rebuild of css when it detects changes. (for this you need a `tailwindcss`-binary in your path, e.g. `/usr/bin/tailwindcss`)
- You don't need to `tailwindcss -i ./assets/css/input.css -o ./assets/css/output.css` and linking the stylesheets to `output.css` before you build hugo.


```go
{{ with resources.Get "css/base.css" }}
  {{ $opts := dict "minify" true }}
  {{ with . | css.TailwindCSS $opts }}
    {{ if hugo.IsDevelopment }}
      <link rel="stylesheet" href="{{ .RelPermalink }}">
    {{ else }}
      {{ with . | fingerprint }}
        <link rel="stylesheet" href="{{ .RelPermalink }}" integrity="{{ .Data.Integrity }}" crossorigin="anonymous">
      {{ end }}
    {{ end }}
  {{ end }}
{{ end }}

```
If you wan't to turn off/on Tailwind for your css, just remove/add the following from/to the top of your `base.css`.
```css
@import "tailwindcss";
```
### Where does Hugo search for tailwindcss?
If you use the **binary** (https://tailwindcss.com/blog/standalone-cli) instead of the **npm package**, you might
come across the problem of hugo not finding it probably. The error might look like this:
```bash
ERROR TAILWINDCSS: failed to transform "/css/base.css" (text/css): Error: Failed to find 'tailwindcss'
  in [
    C:\Users\user\repo
  ]
    at C:\snapshot\tailwindcss\node_modules\postcss-import\lib\resolve-id.js:35:13
    at async LazyResult.runAsync (C:\snapshot\tailwindcss\node_modules\postcss\lib\lazy-result.js:261:11)
    at async build (C:\snapshot\tailwindcss\lib\cli\build\index.js:49:9)
Built in 5708 ms
```
This is because your tailwind-binary isn't registered in the PATH of your system.

- Windows: Search for `env` in the searchbar, and add the location of tailwind to your user-variables.
- Linux: Add location to your `$PATH` in your `.profile` or `.bashrc`

If you are interested in which order hugo searches for tailwind; here is the LoC regarding this behaviour:
https://github.com/gohugoio/hugo/blob/master/common/hexec/exec.go#L185



- Docs: https://gohugo.io/functions/css/tailwindcss/

## Custom Output Formats
You can generate all kinds of different data-structures with hugo. This can be helpful when making the sites available for other programs (e.g. search-function).


If you want generate `search.json`, which will be available at `/`, you need two things.


- The configuration for a custom outputFormat in your `hugo.toml`
- and a template for generating the content of `search.json`


The following is the config, that needs to be added to ypur `hugo.toml`.
```toml
[outputFormats]
  [outputFormats.Search]
  mediaType = 'application/json'
  baseName = 'search'
  isPlainText = true

[outputs]
home = ['HTML','Search']
```
Besides the custom format `Search`, home also needs the instruction to generate `HTML`.
Otherwise just the custom format would be generated. That's why both are declared.


`outputs.<kind>` needs a corresponding template in `layouts/_default`. In this case, with your Search-Format, it would be `home.search.json`.
Without the custom output format the templates name would be `home.json.json`, which would generate `index.json` at `/`.


> In a way the custom output format is just a way to **alter the name of the generated file**.


In the `home.search.json`-template you can declare all your needed data.
```go
[
{{- $first := true -}}
{{- range .Pages -}}
  {{- if not $first -}},{{- end -}}
  {
    "title": {{ .Title | jsonify }},
    "url": {{ .Permalink | jsonify }},
    "content": {{ .Plain | jsonify }}
  }
  {{- $first = false -}}
{{- end -}}
]
```
- Reason for the name-schema of `home.json.json` and `home.search.json`: https://gohugo.io/templates/output-formats/#template-lookup-order

## Themes I might check out

- https://github.com/nodejh/hugo-theme-mini

## Troubleshooting and errors

### `ÄÖÜäöü` won't render correctly
Adding the charset to the `head.html` helps.
```html
<meta charset="UTF-8">
```
### "I want to see the all properties of an object."
You will get what you want with: `{{ debug.Dump . }}`.
The dot will print the context your in, but you can also change it to a variable.
