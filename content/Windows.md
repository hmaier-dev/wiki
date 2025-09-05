---
title: Windows
description: You make money with this.
---

## Appx-Packages
Möchte man Appx-Packages installieren unterscheidet man zwischen zwei Arten von Kommando-Gruppen.
Einerseits die Kommandos für `*-AppxPackage` und `*-AppxProvisionedPackage`.

Mit den `AppxPackage`-Kommando kann man im normalen User-Space AppX-Pakete hinzufügen. Diese sind damit auf dem momentan angemeldeten Profil verfügbar.
Möchte man das alle Benutzer dieses Paket erhalten, kann man mit `AppxProvisionedPackage` arbeiten. Bei der Anmeldung wird damit für den jeweiligen Benutzer die App _provisioniert_.

Dabei ist wichtig zu beachten, dass man das `-Online`-Flag nutzt. Damit bearbeitet man die aktuell laufende Windows-Installation. Ohne das `-Online`-Flag kann man ein Windows-Image bearbeiten, muss dann aber den `-Path` mit angeben.
In der Microsoft-Doku gibt es dafür zwei gute Beispiele:

- https://learn.microsoft.com/en-us/powershell/module/dism/add-appxprovisionedpackage?view=windowsserver2025-ps#examples

### Re-register Apps
When some apps fail. try this.
```powershell
Get-AppXPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"}
```

### Desktop Anwendung in MSIX packen

- https://learn.microsoft.com/de-de/windows/msix/packaging-tool/tool-overview

## Drucker-Port/Anschlüsse löschen

- `Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print\Monitors\Standard TCP/IP Port\Ports`

## Drucker löschen

- `Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print\Printers\`

## `Enable-PSRemoting` als GPO

- `Computer Cponfiguration > Administrative Templates > Windows Components > Windows Remote Management (RM) > WinRM Service > Allow remote server management through WinRM`

## Force re-creation of Userprofile
In manchen Fällen kann das Userprofil eines Benutzers beschädigt oder anders korrupiert sein.
Um dies zu beheben, muss man in folgenden Registrypfad gehen und das betreffende Profil löschen:

- `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList`

- https://superuser.com/questions/512484/how-do-i-force-windows-7-to-create-a-new-domain-profile-with-same-name-as-an-exi

## Sound Settings

Hier kommt man ins alte Sound-Menü `mmsys.cpl`.
