---
title: Sysprep
---
Natives Windows-Programm zur Vorbereitung einer Installation, bevor man ein Image zieht.

## Bitlocker
Bitlocker verhindert das Generalisieren von Sysprep. Entweder man schaltet Bitlocker über die Einstellungen
aus (`Einstellungen > Update & Sicherheit > Geräteveschlüsselung`) oder 
man nutzt das cmd-Programm `manage-bde` mit `manage-bde -off C:`. Mit `manage-bde -status`
kann man den Status aller Laufwerke einsehen.
