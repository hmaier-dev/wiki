---
title: oscdimg.exe
---

## install.wim in ISO verpacken

Dafür benötigt man `oscdimg.exe`, welches im _Windows Assessment and Deployment Kit_ enthalten ist. Herunterladen kann man die ADK über folgenden Link

- https://learn.microsoft.com/en-us/windows-hardware/get-started/adk-install

Der Standard-Installationpfad von `oscdimg.exe` ist folgender:

- `%ProgramFiles(x86)%\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools\amd64\Oscdimg`

Außerdem benötigt man eine funktionierende Standard Windows ISO. Nun müssen folgende Schritte gegangen werden.

- Per `7zip` die ISO entpacken und nach `sources` navigieren.
```cmd
C:\Win10_22H2_German_x64v1\sources
```
- Dort die alte `install.wim` gegen die neue tauschen.
- Die ISO neu bauen.

Da Oscdimg by default nicht in den Umgebungvariablen ist, sucht man nach _Umgebung für Bereitstellungs- und Imageerstellungstools_ und start das Programm dann mit administrativen Rechten.
Der Pfad in den man geworfen wird ist folgender: `C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools`. Dort kann man dann folgendes Kommando ausführen.
```cmd
oscdimg -bC:\Win10_22H2_German_x64v1\boot\etfsboot.com -u2 -h -m -lCUSTOM_WIN C:\Win10_22H2_German_x64v1 C:\CustomWindows.iso
```


Die Infos dieses Absatzes hab ich aus diesem Artikel: https://www.windowspro.de/wolfgang-sommergut/bootfaehige-iso-fuer-windows-image-wim-erstellendocx

## Troubleshooting
### Error 5
Starte _Umgebung für Bereitstellungs- und Imageerstellungstools_ mit administrativen Rechten.
