# Powershell
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


