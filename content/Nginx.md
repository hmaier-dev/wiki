---
title: Nginx
---

## Reverse Proxy
Ein gängies Setup beim Umgang mit Docker-Containern ist, vor diese einen Reverse Proxy zu schalten.
Eine einfache Config die auf Port 80 lauscht und an Port 8080 weiterleitet, kann so aussehen:

```conf
server {
    server_name my-server-com;
    listen 80;
    listen [::]:80;
    location / {
        proxy_pass http://localhost:8080;
        proxy_redirect                      off;
        proxy_set_header  Host              $http_host;
        proxy_set_header  X-Real-IP         $remote_addr;
        proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto $scheme;
        proxy_read_timeout                  900;
    }
}
```


## SSL
Mit `certbot` lässt sich SSL relativ einfach ab-frühstücken.
### Sub-Domäne zu bestehenden Zertifikat hinzufügen
Bevor man eine neue (Sub-)Domäne zum Zertifikat hinzufügt, muss der DNS-Eintrag schon live sein.
```bash
certbot --expand -d existing.com -d www.exisiting.com -d newdomain.com
```
- https://eff-certbot.readthedocs.io/en/latest/using.html#re-creating-and-updating-existing-certificates

## Static html
Wenn man mit statischen HTML-Seiten hantiert und einen `403` erhält, kann man sich ziemlich sein, dass etwas mit den Permissions nicht stimmt.
Daher den Owner sowie die Permissions der *ganzen* Directory überprüfen:
```bash
ls -la /var/www/html/static-html
sudo chmod -R 755 /var/www/html/static-html`
sudo chown www-data:www-data /var/www/html/static-html`
```
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

## static-html plus reverse-proxy

```
server {

    server_name localhost;

    location /preview/ {
      alias /var/www/html/static-html/;
      index index.html;
      try_files $uri $uri/ =404;

    }
    error_page 404 /404.html;

    location / {
        proxy_pass http://localhost:8080;
        proxy_redirect                      off;
        proxy_set_header  Host              $http_host;
        proxy_set_header  X-Real-IP         $remote_addr;
        proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto $scheme;
        proxy_read_timeout                  900;
    }

  access_log /var/log/nginx/wordpress_access.log;
  error_log /var/log/nginx/wordpress_error.log;
}
~
```
