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

## Windows 11 on unsupported Hardware
Mit diesem Script hat es gut funktioniert: https://gist.github.com/asheroto/5087d2a38b311b0c92be2a4f23f92d3e

## Drucker
Um die Druckerwarteschlange abzuhören, bzw. zu loggen, kann man folgendes Powershell-Skript nutzen:
```powershell
## Diese Attribute findet man unter: https://learn.microsoft.com/de-de/windows/win32/cimwin32prov/win32-printjob#syntax
## All Atributes of Win32_PrintJob
# $job.TimeSubmitted
# $job.Caption
# $job.Description
# $job.Document
# $job.HostPrintQueue
# $job.JobId
# $job.JobStatus
# $job.Name
# $job.Notify
# $job.Owner
# $job.PagesPrinter
# $job.PaperLength
# $job.PaperSize
# $job.PaperWidth
# $job.TotalPages
# $job.Color
# $job.DataType
# $job.DriverName

$LogFile = "C:\Users\superSpecialUser\Desktop\PrintJobLog.txt"
if (-not (Test-Path $LogFile)) {
    New-Item -Path $LogFile -ItemType File -Force | Out-Null
}
try {
    $create = "JobCreation"
    Register-WmiEvent -Query "SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_PrintJob'" -SourceIdentifier $create -Action {
      $job = $Event.SourceEventArgs.NewEvent.TargetInstance
      $action = "NEW JOB"
      $raw = $job.TimeSubmitted.Substring(0,14)
      $dt = [datetime]::ParseExact($raw, "yyyyMMddHHmmss", $null)
      $time = $dt.ToString("yyyy-MM-dd_HH-mm-ss")
      $msg = "$($time) => [$($action)] | $($job.Caption) $($job.HostPrintQueue) $($job.Owner) $($job.Document) ($($job.JobId))"
      Write-Host $msg
      $msg | Out-File "C:\Users\superSpecialUser\Desktop\PrintJobLog.txt" -Append
  
    }

    $remove = "JobRemoved"
    Register-WmiEvent -Query "SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_PrintJob'" -SourceIdentifier $remove -Action {
      $job = $Event.SourceEventArgs.NewEvent.TargetInstance
      $action = "JOB REMOVED"

      $raw = $job.TimeSubmitted.Substring(0,14)
      $dt = [datetime]::ParseExact($raw, "yyyyMMddHHmmss", $null)
      $time = $dt.ToString("yyyy-MM-dd_HH-mm-ss")
      $msg = "$($time) => [$($action)] | $($job.HostPrintQueue) $($job.Owner) $($job.Document) ($($job.JobId))"
      Write-Host $msg
      $msg | Out-File "C:\Users\superSpecialUser\Desktop\PrintJobLog.txt" -Append
    }


    Write-Host "Monitoring for new processes. Press Ctrl+C to stop."
    # Use a loop to keep the script running and the session active.
    while ($true) {
        Start-Sleep -Seconds 5
    }

} finally {
    Write-Host "Unregister and remove: $create"
    Unregister-Event -SourceIdentifier $create
    Get-Job -Name $create | Remove-Job -Force

    Write-Host "Unregister and remove: $remove"
    Unregister-Event -SourceIdentifier $remove
    Get-Job -Name $remove | Remove-Job -Force
}
```

## WMI
Diese verschiedenen Objekte kann man mit WMI abhören:

- https://learn.microsoft.com/de-de/windows/win32/cimwin32prov/computer-system-hardware-classes

Unter den verschiedenen Klassen findet man den jeweils die Attribute.


## Installers
On Windows there are several installers types, which enable the admin to rollout the software in different ways.
### NSIS
https://nsis.sourceforge.io/Main_Page
### MSI
Mit der Windows ADK erhält man hilfreiche Einblicke in MSI-Pakete:
- https://developer.microsoft.com/de-de/windows/downloads/windows-sdk/
