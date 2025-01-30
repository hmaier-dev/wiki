---
title: Wordpress
---


Die folgende Anleitungen leiten im Theme _Twenty Seventeen_ an. 

## Wie ändere ich das Header-Bild einer Seite?
1. Im Admin-Dashboard auf `Seiten > Alle Seiten` gehen und die betreffende Seite `Bearbeiten`.
2. Auf das blaue Plus auf der oberen linken Seite drücken, was dem Block-Inserter erscheinen lässt.
3. Im Suchfeld oder manuell (Unterpunkt: Theme) nach `Beitragsbild` suchen und darauf klicken.
4. Das aktuelle Beitragsbild/Header-Bild erscheint im Editor und lässt sich mit einem Klick auf die drei Punkte ändern.

- Möchte man es entfernen, muss man statt `Löschen` auf `Zurücksetzen` gehen.

## Wie ändere ich die Startseite?
1. Im Admin-Dashboard auf `Design > Customizer` gehen.
2. Unter `Theme-Optionen` und `Inhalt im Startseiten-Abschnitt 1-5` kann man die verschiedene Seiten auswählen, die auf der Startseite angezeigt werden sollen.

## Wie ändere ich die URL einer Seite?

1. Im Admin-Dashboard auf `Seiten > Alle Seiten` gehen.
2. Mit der Maus über den Listeneintrag der Seiten fahren.
3. `QuickEdit` auswählen.
4. In dem Feld `Titelform` lässt sich der Name der Seite in der URL ändern.



## Errors 

### Der Server kann das Bild nicht verarbeiten. Dies kann vorkommen, wenn der Server beschäftigt ist oder nicht genug Ressourcen hat, um die Aufgabe abzuschließen. Es könnte helfen, ein kleineres Bild hochzuladen. Die maximale Größe sollte 2560 Pixel nicht überschreiten. 

Wahrscheinlich ist das Bild im Format `.jpeg` oder `.png` vorhanden.
Hier kann eine Konvertierung zu `.webp` helfen.

``` bash
cwebp -q 80 bild.jpg -o bild.webp 
```

Damit wird das Bild verkleinert und \"sichtbarer\" (?) für Suchmaschinen
gemacht.

## Ressourcen

- Basic Setup: <https://ubuntu.com/tutorials/install-and-configure-wordpress#1-overview>
