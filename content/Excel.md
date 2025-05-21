---
title: Microsoft Excel
---
I am truly sad to write this article. I arrived in Corporate hell.

## FAQ

- How to reset all filters:
    - `CTRL+SHIFT+L`

## default paste without format

https://support.microsoft.com/en-us/office/control-the-formatting-when-you-paste-text-20156a41-520e-48a6-8680-fb9ce15bf3d6

## Vordefinierte Spalten als Drop-Down-Menü

Um die Dateneinträge sauber zu halten, bietet es sich an für eine Spalte ein vordefiniertes Drop-Down-Menü zu verwenden.
Dazu nimmt eine eine separate Tabelle und definiert dort die vorgegebenen Werte. Diese wählt man dann aus und wählt mit einem Rechtsklick den Punkt `Namen definieren` aus.

In der Haupttabelle wählt man dann mitm `STRG+SPACE` die gesamte Spalte aus. Unter `Daten > Datentools` findet man `Datenüberprüfung`.
Dort kann man unter `Einstellungen` `Zulassen: Liste` auswählen. Als Quelle gibt man dann den definierten namen an, z.B.: `=Status`.

Möchte man die Werte des Drop-Down-Menüs ändern, muss man in der separaten Tabelle erst den Wert hinzufügen und kann dann über den `Namens-Manager` den _erfassten Bereich_ ändern.
Den `Namens-Manager` findet man entweder über die Suche oder unter `Formeln > definierte Namen > Namens-Manager`.

