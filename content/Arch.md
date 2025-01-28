---
categories:
- linux
title: Arch
---

# Arch Linux

{{< single-image src="media/blahaj-close-shot.webp" >}}

## Dualbooting with Windows 

With `systemd-boot` it is relativly easy to install Linux and Windows
alongside. My suggestion would be to install Linux first and then make
space for the Windows install. `systemd-boot` will automatically find
all UEFI-partitions to boot from.

Over the time, problems can occure because Windows will do ugly things
to foreign partitions, when it updates. So be prepared.

### `Error Preparing initrd: Volume corrupted` 

The Windows install will probably still boot.

1.  Boot with a live medium.
2.  Make a filesystem-check on the boot partition and approve the
    fix-prompt with: `fsck /dev/sda1`
3.  Re-generate the boot-image with: `mkinitcpio -P`
4.  Reboot.

## `pacman`

To ignore updates/replacement for a package, you can add it under
options, e.g.:

``` bash
[options]
IgnorePkg = ttf-sourcecodepro-nerd
```

I already have `nerd-fonts-source-code-pro` installed via the AUR, so I
ignore the native arch-package.

- How to find non-used packages (orphans)?
    - `alias lsorphans="sudo pacman -Qdt"`
- How to remove non-used packages (orphans)?
	- `alias rmorphans="pacman -Qtdq | sudo pacman -Rns -"`

## Network
You can do it different ways. Gnome uses `NetworkManager` by default.
A less bloated way would be using the `systemd`-daemons for DNS and DHCP: `systemd-networkd` and `systemd-resolved`.
Running the following script with the fitting `$interface` will give a basic config for using the network.
```bash
interface=eno1
touch /etc/systemd/network/20-wired.network
echo "[Match]" >> /etc/systemd/network/20-wired.network
echo "Name=$interface " >> /etc/systemd/network/20-wired.network
echo " " >> /etc/systemd/network/20-wired.network
echo "[Network]" >> /etc/systemd/network/20-wired.network
echo "DHCP=yes" >> /etc/systemd/network/20-wired.network
```

### Static IP
If your IP does not change, you can skip DHCP in the boot-process. You can configure a static IP as following
in `/etc/systemd/network/20-wired.network`.
```toml
[Match]
Name=eno1 
 
[Network]
Address=192.168.178.110/24
Gateway=192.168.178.1
DNS=192.168.178.1
```

