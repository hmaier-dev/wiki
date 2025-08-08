---
title: dism.exe
---
Tool zur Imageverwaltung für die Bereitstellung

## Capture einer Installation
Nach dem man die Installation mit `sysprep.exe` vorbereitet hat, booten man in eine WinPE-Umgebung
und kann von dort das ein `/capture-image` anstoßen.
```cmd
Dism /capture-image /imagefile:D:\install-win10.wim /CaptureDir:C:\ /Name:"Custom Windows 10 Image"
```
Der Speicherort des `/imagefile` solle nach dem Herunterfahren der WinPE weiterhin erreichbar sein. Man nehme beispielweise einen USB-Stick oder mountet ein Netzlaufwerk.

### WinPE
Zum Booten empfehle ich [Venoty](https://www.ventoy.net/en/index.html) und als WinPE-Umgebung [PhoenixPE]({{% ref path="phoenixpe" %}}).

## Mount install.wim
Um Dateien einer `install.wim` hinzuzufügen, ist es nötig diese zu mounten.
```cmd
dism /Mount-Wim /WimFile:"C:\Werkstatt_Service_Rechner\install.wim" /index:1 /MountDir:C:\mount
```
Nach Abschluss der Arbeiten am Image, kann man wie folgt unmounten:
```cmd
dism /Unmount-Wim /MountDir:C:\mount /Commit
```

## Features Offline hinzufügen
Möchte man Features direkt nach der Installation verfügbar haben, kann man diese mit `dism.exe` vor der Installation dem Image hinzufügen.

Dafür benötigt man die `install.wim` die man unter `\sources\install.wim` findet. Diese hängt man nun mit folgenden Kommando ein.
```cmd
dism /Mount-Wim /WimFile:"C:\W10_WST_1\install.wim" /index:1 /MountDir:C:\mount
```
Danach kann man sich erstmal alle Features anzeigen lassen.
```cmd
DISM /Image:c:\mount /Get-Features /Format:Table
```
Möchte man bspw. .NET 3.5 aktiviert haben, führt man nun folgendes Kommando aus.
```cmd
dism /Image:C:\mount /Enable-Feature /FeatureName:NetFx3 /All /Source:C:\Win10_22H2_German_x64v1\sources\sxs /LimitAccess
```
Als Source braucht man die Installationsquellen. Diese findet man in einer Windows-ISO unter `\sources\sxs`.

Nun kann man das Feature an sich nochmal abfragen, um sicherzugehen, dass es dem Image korrekt hinzugefügt worden ist.
```cmd
dism /Image:C:\mount /Get-FeatureInfo /FeatureName:NetFx3
```
Zum Ende der Arbeiten an der `install.wim` muss man sie unmounten.
```cmd
dism /Unmount-Wim /MountDir:C:\mount /Commit
```
Um nun eine bootfähige ISO zu erhalten, nutzt man [oscdimg.exe]({{% ref path="oscdimg" %}}).


## Troubleshooting
### Error 1243
Kann beim mounten einer `install.wim` auftreten. Mit diesen Registry-Einträgen kann man den Fehler lösen:
```cmd
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WIMMount]
"DebugFlags"=dword:00000000
"Description"="@%SystemRoot%\\system32\\drivers\\wimmount.sys,-102"
"DisplayName"="@%SystemRoot%\\system32\\drivers\\wimmount.sys,-101"
"ErrorControl"=dword:00000001
"Group"="FSFilter Infrastructure"
"ImagePath"=hex(2):73,00,79,00,73,00,74,00,65,00,6d,00,33,00,32,00,5c,00,64,00,\
72,00,69,00,76,00,65,00,72,00,73,00,5c,00,77,00,69,00,6d,00,6d,00,6f,00,75,\
00,6e,00,74,00,2e,00,73,00,79,00,73,00,00,00
"Start"=dword:00000003
"SupportedFeatures"=dword:00000003
"Tag"=dword:00000001
"Type"=dword:00000002

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WIMMount\Instances]
"DefaultInstance"="WIMMount"

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WIMMount\Instances\WIMMount]
"Altitude"="180700"
"Flags"=dword:00000000
```
Quelle ist dieser Artikel: https://answers.microsoft.com/en-us/windows/forum/all/solved-dismexe-error-1243-the-specified-service/836b860c-6427-40f9-9ea8-21869cd1218d

Warum das funktioniert, ist mir nicht bekannt.

### Error 161

Die Meldung dazu ist: `Der angegebene Pfadname ist ungültig.`
Nach einen `chdsk` auf Quelle und Ziel funktioniert `dism.exe`.
```cmd
chdsk E: /f
chdsk G: /f
dism /capture-image /imagefile:E:\image_folder\image1.wim /capturedir:G:\ /Name:"w7-important-image"
```
