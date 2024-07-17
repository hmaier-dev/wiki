# Wordpress 

-   <https://ubuntu.com/tutorials/install-and-configure-wordpress#1-overview>

# Errors 

## Der Server kann das Bild nicht verarbeiten. Dies kann vorkommen, wenn der Server beschäftigt ist oder nicht genug Ressourcen hat, um die Aufgabe abzuschließen. Es könnte helfen, ein kleineres Bild hochzuladen. Die maximale Größe sollte 2560 Pixel nicht überschreiten. 

Wahrscheinlich ist das Bild im Format `.jpeg` oder `.png` vorhanden.
Hier kann eine Konvertierung zu `.webp` helfen.

``` bash
cwebp -q 80 bild.jpg -o bild.webp 
```

Damit wird das Bild verkleinert und \"sichtbarer\" (?) für Suchmaschinen
gemacht.
