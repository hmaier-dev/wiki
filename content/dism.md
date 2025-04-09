---
title: dism.exe
---
Tool zur Imageverwaltung für die Bereitstellung

## Mount install.wim
Um Dateien einer `install.wim` hinzuzufügen, ist es nötig diese zu mounten.
```cmd
dism /Mount-Wim /WimFile:"C:\Werkstatt_Service_Rechner\install.wim" /index:1 /MountDir:C:\mount
```
Nach Abschluss der Arbeiten am Image, kann man wie folgt unmounten:
```cmd
dism /Unmount-Wim /MountDir:C:\mount /Commit
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
