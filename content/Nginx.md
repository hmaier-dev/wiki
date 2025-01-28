---
categories:
- Web-Development
title: Nginx
---

# Nginx

## SSL
Mit `certbot` lässt sich SSL relativ einfach ab-frühstücken.
### Sub-Domäne zu bestehenden Zertifikat hinzufügen
Bevor man eine neue (Sub-)Domäne zum Zertifikat hinzufügt, muss der DNS-Eintrag schon live sein.
```bash
certbot --expand -d existing.com -d www.exisiting.com -d newdomain.com
```
- https://eff-certbot.readthedocs.io/en/latest/using.html#re-creating-and-updating-existing-certificates

## Alias
Mit `alias` kann man Pfad bereitstellen, der nicht mit der `location` zusammenpasst. Fordert man mit der `root`-Direktive den Pfad `/preview/workshops/index.html` an,
würde Nginx nach `/var/www/html/static-html/preview/workshops/index.html` suchen. Die angeforderte URI wird also *appended*.
Bei der folgenden Directory-Struktur würde man aber nix finden:
```bash
static-html
├── about-me
│   └── index.html
├── css
│   └── style.css
├── favicon.ico
├── index.html
├── index.xml
└── workshops
    └── index.html

```
Mit der `alias`-Direktive wird der `/preview/`-Teil nicht mit angefordert, man kommt also `/var/www/html/static-html/preview/workshops/index.html` heraus.

Für mehr, hier ist eine gute Erklärung auf StackOverflow:

- https://stackoverflow.com/questions/10631933/nginx-static-file-serving-confusion-with-root-alias


## Status Codes

A status code is more than a number.

- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

When troubleshooting use `curl -I <url>` to get unfiltered insights into the reponse.

### `403`
Wenn man einen `403` erhält, kann man sich ziemlich sein, dass etwas mit den Permissions nicht stimmt.
Daher den Owner sowie die Permissions der *ganzen* Directory überprüfen:
```bash
ls -la /var/www/html/static-html
sudo chmod -R 755 /var/www/html/static-html`
sudo chown www-data:www-data /var/www/html/static-html`
```
## Configs

### Static HTML
 
This config just serves static html under the path `/preview`. 

#### `alias`
When you want an URI with a different path in the filesystem, 
e.g. `/var/www/html/static-html/page1/index.html` but not `/var/www/html/static-html/preview/page1/index.html`,
then `alias` is your directive of choice.

#### `index`
Tells Nginx for which files to look, when a directory is requested. In this case `index` directs a directory-request to `index.html`.
Without it `http://localhost/preview/site1` would not work and would need `http://localhost/preview/site1/index.html`.
Technically, if you have `try_files` setup that it directs to `index.html`, you wouldn't need it.

#### `try_files`
Looks for the different cases defined. Note that this hinders a redirect!

1. `$uri` just takes the URI as it is. `http://localhost/preview/index.html` would connect, but `http://localhost/preview/` not.
2. `$uri/index.html` append the `index.html`. As it is the second case, existent URI with or without `index.html` would get `200`.
3. If nothing fits the schema, do a `404` response.

Because of `$uri/index.html`, `http://localhost/preview` (without a trailing slash) as well as `http://localhost/preview/` (with a trailing slash) will work!
```nginx
server {
    server_name localhost;
    
    location /preview {
      alias /var/www/html/static-html;
      index index.html;
      try_files $uri $uri/index.html =404;
    }

    error_page 404 /404.html;

    access_log /var/log/nginx/website_access.log;
    error_log /var/log/nginx/website_error.log;
}

```


### Reverse-Proxy with Docker-Container
```nginx
server {

    server_name localhost;

    location / {
        proxy_pass http://localhost:8080;
        proxy_redirect                      off;
        proxy_set_header  Host              $http_host;
        proxy_set_header  X-Real-IP         $remote_addr;
        proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto $scheme;
        proxy_read_timeout                  900;
    }

  access_log /var/log/nginx/docker_access.log;
  error_log /var/log/nginx/docker_error.log;
}
```

#### Header

- `proxy_set_header  Host              $http_host;`
- `proxy_set_header  X-Real-IP         $remote_addr;`
- `proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;`
- `proxy_set_header  X-Forwarded-Proto $scheme;`
    - Set the protocol to `http` or `https`
