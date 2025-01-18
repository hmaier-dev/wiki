---
categories:
- Web-Development
title: htmx
---

# Basis 

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

# Errorhandling 

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
