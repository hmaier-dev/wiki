# Hugo
Is a generator for static html. 
## Configuration
You will need several things for Hugo.

- a `./content`-directory with your knowlegde written in markdown (`.md`)
- some layout files under `./layouts/_default`, so Hugo knows how to structure the site
- and a config file, which can be `toml`, `json` or something else 

### Layouts
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
- `single.html`

``` html
{{ define "main" }}
    {{.Content}}
{{ end }}
```
If you have worked with the Golang-modules `html/template` or `text/template`, this should look familiar to you.


### Config-file

Hugo needs config-file, which default is `hugo.toml`.
```toml
baseURL = "https://hmaier-dev.github.io/wiki/"
languageCode = "de-us"
title = "Wiki"
```

