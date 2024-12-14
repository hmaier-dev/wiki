# systemd

## mount units 

Um zu vermeiden in der `/etc/fstab` herumzupfuschen, kann man
alternative (auto-)mount.units verwenden. Folgendes Schema ist dabei
einzuhalten:

-   /etc/systemd/system/path-to-mount.mount
-   /etc/systemd/system/path-to-mount.automount

``` systemd
## path-to-mount.automount
[Unit]
Description=Automount networkshare

[Automount]
Where=/path/to/mount

[Install]
WantedBy=multi-user.target
```

``` systemd
## path-to-mount.mount
[Unit]
Description=some networkshare
Wants=network-online.target
After=network-online.target

[Mount]
What=//192.168.137.42 
Where=/path/to/mount
Type=cifs
Options=credentials=/home/user/.smbcredentials,vers=2.1,noserverino,uid=1000,gid=1000

[Install]
WantedBy=multi-user.target
```

Source: [Mount Network Drive with systemd on
Startup](https://unix.stackexchange.com/questions/684937/mount-network-drive-with-systemd-on-startup/691576#691576)

## systemd-boot

An einigen Rechner kann es vorkommen, dass `bootctl install` mit
folgender Fehlermeldung fehlschlägt:

``` cmd
Unable to write 'LoaderSystemToken' EFI variable
```

Dies sei laut systemd Github-Issue ein Hardware-Problem. Umgehen kann
man dies in dem man die Flag `--graceful` anhängt.

``` bash
bootctl install --graceful
```

Damit verhindert man das Abbrechen bei Fehlern.
