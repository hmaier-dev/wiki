---
categories:
- Windows
title: Powershell
---

A collection of some powershell-snippets I found useful, can be found under:

- https://github.com/hmaier-dev/powershell-library/tree/main/src

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

## Get all line of go

```powershell
Get-ChildItem -Recurse -Include '*.go' | Get-Content | Measure-Object -Line
```
