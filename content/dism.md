---
title: dism.exe
description: Deployment Image Servicing and Management. Clean out Windows from Dirt with this.
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

## Wim-File mounten
Um Dateien einer wim-Datei hinzuzufügen oder eine ISO daraus zu erstellen, ist es nötig diese zu mounten.
```cmd
dism /Mount-Wim /WimFile:"C:\Werkstatt_Service_Rechner\install.wim" /index:1 /MountDir:C:\mount
```
Die Windows-Installation ist nun unter C:\mount verfügbar.

Nach Abschluss der Arbeiten am Image, kann man wie folgt unmounten:
```cmd
dism /Unmount-Wim /MountDir:C:\mount /Commit
```

## Apply einer Installation
Hat man mit `/Capture-Image` ein Abbild aufgenommen,
kann man es mit `/Apply-Image` direkt (ohne Erstellen einer ISO) auf eine Partition anwenden.
```cmd
dism /Apply-Image /ImageFile:E:\imagefiles\W7.wim /Index:1 /ApplyDir:C:\
```
Dafür bietet es sich an sich über eine WinPE auf das System aufzuschalten.
Von dort aus kann man das Wim-File auf die C:\-Partition anwenden.

Gibt es hier die Meldung `Der angegebene Pfadname ist ungültig.` muss man ein `chkdsk` auf Quelle/Ziel anwenden.

## Get-WimInfo
In einem WimFile können mehrere Windows-Versionen sein. Z.B.: Home aber auch Pro.
Diesen werden durch einen Index gekennzeichnet.
```cmd
dism /Get-WimInfo /WimFile:C:\Win7_Clean\install.wim
```
Es werden nun die verschiedenen Windows-Versionen inklusive Größe und Index ausgegeben.
```cmd

Tool zur Imageverwaltung für die Bereitstellung
Version: 10.0.26100.5074

Details für Abbild: "C:\Win7_Clean\install.wim"

Index: "1"
Name: "Windows 7 Home Basic"
Beschreibung: "Windows 7 Home Basic"
Größe: 11.623.452.494 Bytes

Index: "2"
Name: "Windows 7 Home Premium"
Beschreibung: "Windows 7 Home Premium"
Größe: 12.136.659.100 Bytes

Index: "3"
Name: "Windows 7 Professional"
Beschreibung: "Windows 7 Professional"
Größe: 12.037.929.390 Bytes

Index: "4"
Name: "Windows 7 Ultimate"
Beschreibung: "Windows 7 Ultimate"
Größe: 12.200.638.813 Bytes

Der Vorgang wurde erfolgreich beendet.
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

## Export einer Windows Version
In der ISO die man von Microsoft herunterlädt, sind zahlreiche verschiedene Windows Versionen enthalten. Um ein Wim-File mit der einzigen gewollten Version zu erhalten, kann man diese Exportieren.
```
dism /Export-Image /SourceImageFile:"D:\sources\install.wim" /SourceIndex:2 /DestinationImageFile:"D:\sources\install_clean.wim" /Compress:max /CheckIntegrity
```


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
chkdsk E: /f
chkdsk G: /f
dism /capture-image /imagefile:E:\image_folder\image1.wim /capturedir:G:\ /Name:"w7-important-image"
```
