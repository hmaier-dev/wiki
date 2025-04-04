---
title: Sysprep
---
Natives Windows-Programm zur Vorbereitung einer Installation, bevor man ein Image zieht.

## Bitlocker
Bitlocker verhindert das Generalisieren von Sysprep. Entweder man schaltet Bitlocker über die Einstellungen
aus (`Einstellungen > Update & Sicherheit > Geräteveschlüsselung`) oder 
man nutzt das cmd-Programm `manage-bde` mit `manage-bde -off C:`. Mit `manage-bde -status`
kann man den Status aller Laufwerke einsehen.

## Capture mit `dism.exe`
Nach dem man die Installation mit `sysprep.exe` vorbereitet hat, booten man in eine WinPE-Umgebung
und kann von dort das ein `/capture-image` anstoßen.
```cmd
Dism /capture-image /imagefile:D:\install-win10.wim /CaptureDir:C:\ /Name:"Custom Windows 10 Image"
```
