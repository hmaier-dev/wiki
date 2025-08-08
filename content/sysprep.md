---
title: sysprep.exe
---
Natives Windows-Programm zur Vorbereitung einer Installation, bevor man ein Image zieht. Normalerweise findet man das GUI-Programm `sysprep.exe` unter `\Windows\System32\Sysprep\`.
Jeglich Logs und Fehlermeldungen die entstehen, findet man im Unterordner `Panther\`.

Möchte man sich ein Image ziehen und auf einem neuen Rechner installieren, empfehlen sich folgende Optionen:

- `OOBE`-Modus: Bei neuen Starten kommt man in die Out-Of-the-Box-Experience, wo man einen neuen User einrichten kann. (Es ist möglich diese mit einer Tastenkombination zu überspringen; bei W7 `STRG+SHITF+F3`)
- `Verallgemeinern`: Damit werden alle Treiber empfehlen.

## Bitlocker
Bitlocker verhindert das Generalisieren via Sysprep. Entweder man schaltet Bitlocker über die Einstellungen
aus (`Einstellungen > Update & Sicherheit > Geräteveschlüsselung`) oder 
man nutzt das cmd-Programm `manage-bde` mit `manage-bde -off C:`. Mit `manage-bde -status`
kann man den Status aller Laufwerke einsehen.

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
