---
categories:
- Web-Development
title: htmx
---

HTMX is a javascript framework which should free the user from writing javscript.
Find out how on the offical website: https://htmx.org/

This is the easiest way to use htmx: https://htmx.org/docs/#download-a-copy

## Basic POST-Request

This is how you basically send an empty POST-request to the
HTTP-Endpoint `/disabled`. Regarding golang, the htmx.min.js doesn\'t
even have to be embedded into the binary.

``` html
<head>
    <script src="/htmx.min.js"></script>
</head>
<body>
    <form hx-post="/disable" >
        <button type="submit" title="Löscht /var/lib/automaintainer/enabled">
            Deaktivieren
        </button>
    </form>
</body>
```

## Errorhandling 

Leider gibt es keine Magie um Errors mit htmx zu behandeln. Allerdings
gibt es htmx-Event mit dem man arbeiten kann.

``` javascript
    document.body.addEventListener('htmx:responseError', function (evt) {
        document.querySelector('body').innerHTML = '';
        document.querySelector('body').innerHTML = evt.detail.xhr.responseText;

        console.log(evt.detail.xhr);
        console.log(evt.detail.elt);
        console.log(evt.detail.target);
        console.log(evt.detail.requestConfig);

    });
```

Bei jeglichem Error wird auf dem Server generiertes HTML in den Body
gepackt.
