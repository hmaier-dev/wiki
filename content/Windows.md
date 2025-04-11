---
title: Windows
---

## Re-register Apps
When some apps fail. try this.
```powershell
Get-AppXPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"}
```

## Drucker-Anschlüsse löschen

- `Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print\Printers\`
