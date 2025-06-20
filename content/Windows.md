---
title: Windows
---

## Re-register Apps
When some apps fail. try this.
```powershell
Get-AppXPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"}
```

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
