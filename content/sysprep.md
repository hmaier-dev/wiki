---
title: sysprep.exe
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

## install.wim in ISO verpacken

Dafür benötigt man `oscdimg.exe`, welches im _Windows Assessment and Deployment Kit_ enthalten ist. Herunterladen kann man die ADK über folgenden Link

- https://learn.microsoft.com/en-us/windows-hardware/get-started/adk-install

Der Standard-Installationpfad von `oscdimg.exe` ist folgender: `%ProgramFiles(x86)%\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools\amd64\Oscdimg`

Außerdem benötigt man eine funktionierende Standard Windows ISO. Nun müssen folgende Schritte gegangen werden.

- Per `7zip` die ISO entpacken und nach `sources` navigieren.
```cmd
C:\Win10_22H2_German_x64v1\sources
```
- Dort die alte `install.wim` gegen die neue tauschen.
- Die ISO neu bauen.

Da Oscdimg by default nicht in den Umgebungvariablen ist, sucht man nach `Umgebung für Bereitstellungs- und Imageerstellungstools` und start das Programm dann mit administrativen Rechten.
Der Pfad in den man geworfen wird ist folgender: `C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools`. Dort kann man dann folgendes Kommando ausführen.
```cmd
oscdimg -bC:\Win10_22H2_German_x64v1\boot\etfsboot.com -u2 -h -m -lCUSTOM_WIN C:\Win10_22H2_German_x64v1 C:\CustomWindows.iso
```


Die Infos dieses Absatzes hab ich aus diesem Artikel: https://www.windowspro.de/wolfgang-sommergut/bootfaehige-iso-fuer-windows-image-wim-erstellendocx

## Troubleshooting

### Package <Package-Name> failed waiting for remove operation

### sysprep not running dlls either the machine is in an invalid state
Der Error sollte so ähnlich aussehen:
```cmd
[0x0f0073] SYSPRP RunExternalDlls:Not running DLLs; either the machine is in an invalid state or we couldn't update the recorded state, dwRet= 1f 
[0x0f00ae] SYSPRP WinMain:Hit failure while processing sysprep cleanup external providers; hr = 0x8007001f
```
Lösen kann man den Fehler, indem man in der Registry folgende Keys ändert.
```powershell
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\Setup\Status\SysprepStatus]
"GeneralizationState"=dword:00000007
"CleanupState"=dword:00000002
```
