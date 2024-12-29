---
title: Nginx
---

# Nginx

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
