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
