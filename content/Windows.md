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
$sourceId = "PrintJob"
try {
    $query = "SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_PrintJob'"
    Register-WmiEvent -Query $query -SourceIdentifier $sourceId -Action {
	$job = $Event.SourceEventArgs.NewEvent.TargetInstance
    $timeSubmitted = $null
    if ($job.TimeSubmitted) {
        # WMI format: yyyymmddHHMMSS.mmmmmm+zzz
        $wmiTime = $job.TimeSubmitted.Substring(0,14)  # yyyymmddHHMMSS
        $timeSubmitted = [datetime]::ParseExact($wmiTime, "yyyyMMddHHmmss", $null)
        $timeSubmitted = $timeSubmitted.ToString("yyyy-MM-dd-HH-mm-ss")
    }

    # Build custom object
    $printJobObj = [PSCustomObject]@{
        TimeSubmitted   = $timeSubmitted
        Caption         = $job.Caption        
        # Description     = $job.Description
        Document        = $job.Document
        DriverName      = $job.DriverName
        HostPrintQueue  = $job.HostPrintQueue
        JobId           = $job.JobId
        JobStatus       = $job.JobStatus
        Name            = $job.Name
        # Notify          = $job.Notify
        Owner           = $job.Owner
        PagesPrinted    = $job.PagesPrinted
        PaperLength     = $job.PaperLength
        PaperSize       = $job.PaperSize
        PaperWidth      = $job.PaperWidth
        TotalPages      = $job.TotalPages
        Color           = $job.Color
        DataType        = $job.DataType
    }

    $printJobObj | ConvertTo-Json -Compress | Out-File ".\PrintJobsLog.json" -Append
    Write-Host "Logged print job: $($job.Document) ($($job.JobId))"

    }
    Write-Host "Monitoring for new processes. Press Ctrl+C to stop."
    # Use a loop to keep the script running and the session active.
    while ($true) {
        # Receive the output from the background job and print it
        Receive-Job -Name $sourceId
        Start-Sleep -Seconds 1
    }
} finally {
    # If error occures or 
    Unregister-Event -SourceIdentifier $sourceId
    Get-Job -Name $sourceId | Remove-Job -Force
}

```
