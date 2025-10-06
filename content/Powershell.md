---
categories:
- Windows
title: Powershell
description: If you need to do Windows; use this.
---

A collection of some powershell-snippets I found useful, can be found under:

- https://github.com/hmaier-dev/powershell-library/tree/main/src

## History
You can get the history of your current powershell session with `Get-History`.
To access older history, you can use the file stored under `(Get-PSReadLineOption).HistorySavePath`.
In this file a maximum of `(Get-PSReadLineOption).MaximumHistoryCount` commands is stored.

With `fzf` you can access this list comfortably:
```powershell
function FuncFuzzySearchHistory(){
  $cmd =  $(Get-Content $((Get-PSReadLineOption).HistorySavePath) | fzf)
  $cmd
  Invoke-Expression $cmd
}
```

## Prompt
To change the behaviour of the powershell prompt before running the command, alter the `prompt`-function.
```powershell
## This sets the window-title with the last three dir of the path
function prompt(){
  $three = (Get-Location).Path -split '\\' | Select-Object -Last 3
  $path = $three[0] + "\" + $three[1] + "\" + $three[2] 
  $host.ui.RawUI.WindowTitle = $path
  "$(Get-Location)> "
}
```

## Constructing an alias with arguments

You can use the builtin-args variable for that.

```powershell
function DotFilesRepo(){
	$base = "git.exe --git-dir=$env:USERPROFILE\repos\dotfiles\ --work-tree=$env:USERPROFILE"
	$cmd = "$base $args" # The $args-variable is builtin and gets all arguments. Discoverd by accident.
	Invoke-Expression -Command $cmd
}

function DotFilesReposStatus(){
    dfr status
}

Set-Alias -Name dfr -Value DotFilesRepo
Set-Alias -Name dfrs -Value DotFilesReposStatus
```

## Aliases

When constructing an alias with the corresponding function, keep in mind that `powershell` is not case-sensitive.
That means, `Set-Alias -Name wiki -Value Wiki` would set alias that overwrites the function.
My approach to this is to add the appropriate verb to the function name, e.g. `Set-Alias -Name wiki -Value EnterWiki`.

## Params

If you want to use flags to activate a function, you can use a `[switch]`.

```powershell

param(
    [switch]$SetTaskScheduler = $False,
)

Write-Host $SetTaskScheduler
if ($SetTaskScheduler){
    Write-Host "Setting the task"
}
```

## Task Scheduler

- nice article: https://www.sharepointdiary.com/2022/06/create-scheduled-task-in-powershell.html

## Credentials Object
If you want to safely pass username and password, you can create a Credentials object
```powershell
$username = "admin1234"
$password = "mysupersecurepassword"

[securestring]$secStringPassword = ConvertTo-SecureString $password -AsPlainText -Force
[pscredential]$cred = New-Object System.Management.Automation.PSCredential ($username, $secStringPassword)

```
## Powershell Data File
Instead of using `json`, `yaml` or another well-known config-file format for your script, you can go the native powershell way with `psd1`-file.

A simple one-dimensional config (e.g. `config.psd1`) would look like this:
```powershell
@{
    Username = "ftp-user"
    Password = "supersecretftppassword"
    Exclude = @("PT*0730*.DAT")
    ## Keep in mind that @() is for array and @{} is for hash table
    Paths = @(
      @{
        Source = 'L:\FileServer\Project1'
        Destination = 'path/to/destination/on/server'
      },
      @{
        Source = 'L:\FileServer\Project2'
        Destination = 'path/to/destination/on/server'
      }
    )
}
```
In your script you would import the config-file and access the variable like properties:
```powershell
$config = Import-PowershellDataFile -Path ".\config.psd1"
$config.Username
$config.Password
$config.Exclude
```

## Prettify Script
For reformatting your scripts, you can use the following project: https://github.com/DTW-DanWard/PowerShell-Beautifier

Run it as following: `Edit-DTWBeautifyScript .\export.ps1` to update the code.

It is available on `scoop` via `scoop install main/powershell-beautifier`.

## LDAP Query
When working with powershell, you most certainly are living in a Windows Domain. With this premise you obviously won't get along without doing some searching in the Active Directoy.
With the following powershell-function you can make ldap-queries by using your current Kerberos Authentification. That means:
1. Logon with your domain-user.
2. Execute the script.
3. Get data without inputting user+password. 
```powershell
function GetUser(){
  param (
    [string]$username
  )
  # Get the current domain name in DN format
  $domain = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
  $domainDN = ($domain.Name -split "\.") -join ",DC=" 
  $domainDN = "DC=$domainDN"

  # Edit this to your needs
  $userPaths = @(
      "OU=Mitarbeiter,OU=IT,OU=Users",
  )
  
  foreach ($path in $userPaths) {
    $full = "LDAP://$path,$domainDN"
    $searcher = New-Object DirectoryServices.DirectorySearcher
    $searcher.SearchRoot = New-Object DirectoryServices.DirectoryEntry($full)
    $searcher.Filter = "(&(objectClass=user)(sAMAccountName=*$username*))"
    $searcher.PageSize = 1000
    $searcher.FindAll() | ? {
      $user = $_.GetDirectoryEntry()
      # If you want to know all properties of an entry
      # you can use this:
      # $user.Properties.PropertyNames | ? { 
      #   Write-Host "$_ : $($user.Properties[$_])"
      # } 
      $out = @"
sAMAccountName:             $($user.samaccountname.Value)
mail:                       $($user.mail)
dn:                         $($user.distinguishedName.Value)
-----------------------------------------
"@
      Write-Host $out
    }
  }
}
```

## CSV Export
For exporting data into a csv, you can use custom powershell-objects and pipe it to the `Export-Csv` function.
```powershell
$results 
foreach ($user in $allUsers) {

        $userObj = [PSCustomObject]@{
            sAMAccountName = $user.sAMAccountName.value
            name = $user.name.value
            mail = $user.mail.value
            dn = $user.distinguishedName.value
        }
        $results += $userObj
    }
}
# Export the results to a CSV file
$results | Export-Csv -Path "UserData.csv" -NoTypeInformation
```

## Delete UserProfiles via Wmi
If you don't have access via `WinRM`, you can use `WMI` (Windows Management Instrumentation) as an Alternative.

Run this as Domain Administrator.
```powershell
## Show all profiles
Get-WmiObject -Computername special_hostname -Class Win32_userprofile
## Show profile
Get-WmiObject -Computername special_hostname -Class Win32_userprofile | Where { $_.LocalPath -like "*domainusername*" }
## Delete the profile
Get-WmiObject -Computername special_hostname -Class Win32_userprofile | Where { $_.LocalPath -like "*domainusername*" } | Foreach { $_.Delete() }
```
You will notice that your user is still present in the LogonUI. Clear out the keys with your username in this Registry-Path:
```cmd
my-remote-machine\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI
```
## Register-WmiEvent
`Wmi` (Windows Management Instrumentation) bietet unter Windows ein Schnittstelle um Informationen über den Zustand des Systems zu erhalten.
Mit Powershell kann `Register-WmiEvent` nutzen, um auf das Eintreten eines Zustands zu reagieren.
Zum Abhören eines Zustands muss man per WQL eine passende Query bauen.

- MS Docs: https://learn.microsoft.com/en-us/windows/win32/wmisdk/wql-sql-for-wmi
- WMI Code Creator: https://www.microsoft.com/en-us/download/details.aspx?id=8572


## Tips and Tricks

### Get all line of go
```powershell
Get-ChildItem -Recurse -Include '*.go' | Get-Content | Measure-Object -Line
```
