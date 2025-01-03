---
title: Arch
---

# Dualbooting with Windows 

With `systemd-boot` it is relativly easy to install Linux and Windows
alongside. My suggestion would be to install Linux first and then make
space for the Windows install. `systemd-boot` will automatically find
all UEFI-partitions to boot from.

Over the time, problems can occure because Windows will do ugly things
to foreign partitions, when it updates. So be prepared.

## `Error Preparing initrd: Volume corrupted` 

The Windows install will probably still boot.

1.  Boot with a live medium.
2.  Make a filesystem-check on the boot partition and approve the
    fix-prompt with: `fsck /dev/sda1`
3.  Re-generate the boot-image with: `mkinitcpio -P`
4.  Reboot.

# `pacman`

To ignore updates/replacement for a package, you can add it under
options, e.g.:

``` bash
[options]
IgnorePkg = ttf-sourcecodepro-nerd
```

I already have `nerd-fonts-source-code-pro` installed via the AUR, so I
ignore the native arch-package.
