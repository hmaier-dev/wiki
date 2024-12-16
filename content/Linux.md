---
title: Linux
---

# Linux {#Linux}

Here I collect interview questions.

### Tell me about some projects your into right now {#Tell me about some projects your into right now}

-   Self-Made Storage Array driven by a raspberry pi
-   Upgrade old MP3-Player (from 3GB to min. 64 GB)
-   1 Year ago I was into hacking old nintendo 3ds
-   I run some custom android rom on my phone (LineageOS)

### How would you connect to a machine in the cloud? {#How would you connect to a machine in the cloud?}

-   `ssh` (Secure Shell, Port 22) is the tool
-   Is there a []{#VPN}**VPN** involved?
-   Is my public-key known to the machine? (auth via ssh-keys)
-   A password is also possible but unsecure, like root-login

### What is does the directory /proc represent? {#What is does the directory /proc represent?}

/proc displays the current state of the kernel, inside the filesystem.
This is possible because everything in linux is treated as a file.

### How to find out the total disk usage? {#How to find out the total disk usage?}

-   `df -h`: for all filesystems, with `-h` for human-readable
-   `du -sh`: for a single directory, `-s` stands for `--summarize`

### How to check for open ports? {#How to check for open ports?}

There are ways to find out the open ports of a system.

-   `netstat`: gets the data from /proc/net
-   `ss`: gets the data from Netlink API from kernel-space

To find the process which opened the port you can use:

-   `netstat`: with the `-tupln` flags the processes are already shown
-   `ss`: same shit

### Check the version of kernel {#Check the version of kernel}

-   `uname -r`

### How to manage services {#How to manage services}

-   `systemctl start <unit>`
-   `systemctl enable <unit>`
-   `systemctl stop <unit>`
-   `systemctl disable <unit>`
-   `systemctl status <unit>`

### How to check for cpu usage? {#How to check for cpu usage?}

-   `ps aux`: `a` means all processes, `x` includes processes not
    associated with a terminal, `u` formats for the output for a user
-   `top`/`htop`: equivalent to the taskmanager

Press `h` in `top` to get help.

#### `top`

-   `t`: cpu usage
-   `m`: memory usage
-   `R`: toogle sorting (desc/asc)

### What filesystems are and which would you choose for which job {#What filesystems are and which would you choose for which job}

-   `NTFS` (New Technology File System): commonly used on Windows
-   `FAT` (File Allocation Table): only small files, commly used for the
    boot-partition
-   `exFAT` (Extended File Allocation Table): like FAT but with bigger
    files
-   `btrfs`
-   `ext4`

### Explain the filesystem hierarchy {#Explain the filesystem hierarchy}

-   `/bin`: binarys for the proper functioning of the system
-   `/sbin`: binarys critical for system administration
-   `/usr`: user-related programs and files

### Find all mounted devices {#Find all mounted devices}

-   `mount`

### What is a init-system? {#What is a init-system?}

The standard init-system as for today is `systemd`. systemd is
responsible for reparenting orphaned processes. To see which init-system
a system runs, go into htop and search for PID 1. If the name of the
binary does not already tell (cuz maybe its just says init), you can use
`file /sbin/init` and see the output which would be
`/sbin/init: symbolic link to ../lib/systemd/systemd`.

### What is a process? {#What is a process?}

A process is nothing but a executing binary. The multiple kind of
processes:

-   user-process: call by the user
-   daemon-process: runs in the background
-   kernel-process: full access to kernel data structures

### What is a user? {#What is a user?}

A user is just a few entry in some config-files:

-   /etc/group

### There is a weird process. Find out things about it {#There is a weird process. Find out things about it}

You can use `top` or `htop` to start the investigation. With PID and
name you could also use `ps aux`. With `lsof -p <PID>` you could see,
which files/sockets are opened by the process.

### Please explain more about `/proc` {#Please explain more about /proc}

In /proc you can see multiple directory named as numbers. These are
processes. More about these things: <https://linuxwiki.de/proc/pid>

-   `cmdline`: command plus arguments which started the process
-   `maps`: memory mapping (which library are used by the process)
-   `cwd`: current working directory of the process
-   `environ`: environment-variables for this process

### Hardlinks and Symlinks {#Hardlinks and Symlinks}

-   Hardlink: ln \<source\> \<dest\>
-   Symlink: ln -s \<source\> \<dest\>

### What are inodes? {#What are inodes?}

Inodes are metadata (filesize, read-write-date, permissions) in the
linux filesystem. In some instances, inodes could occupy more space than
the actual data stored on the system. To find out about inode-usage use
`df -i`.

### Difference between a process and a thread? {#Difference between a process and a thread?}

A thread is a segment of process, which means: a process can hold
multiple threads. Thread are less isolated, which means they share
memory with other threads.

### What command used to find processes as well as cpu and memory usage? {#What command used to find processes as well as cpu and memory usage?}

For memory usage you can use `free -h`. For the cpu usage you could look
at `/proc/stat`. For a nice summary `top` or `htop` would be good.

### How to automize a repeating task? {#How to automize a repeating task?}

You could write script and give it to `cron` or on `systemd`-systems you
could use a unit-file with a `[Timer]`-Section.

### How to find a file? {#How to find a file?}

Usually I would use `locate`. It is faster than `find` because it does
not search in realtime. But I also does not search in realtime. To
update the cache/database `locate` is referring to, type
`sudo updatedb`.

Examples of using `find`:

-   `find / -wholename *nvim/init.lua*`
-   `find /some/path -name someFile -type f`: all files not directorys
-   `find /path/to/search -name "*.jpg" -exec mv {} /destination/path \;`:
    move all .jpg gets moved
-   `find ./ -mtime -7`: files that have been modified in the last seven
    days

### Networking {#Networking}

For troubleshooting the network-connection. You should always have `ip`,
`dhcp` and `dns` in mind.

-   What is my ip-address? =\> `ip addr`
-   Where is my gateway? =\> usually at the `.1`
-   Is my default route configured? =\> `ip route` look for
    `default via ...`
-   What is my name-server for dns? =\> look into /etc/resolv.conf
-   Are there any services handling `dhcp` and `dns`?
    -   For `dhcp`: `systemd-networkd` or `dhcpcd`
    -   For `dns`: `systemd-resolved` or `dhcpcd`

#### Find out the mac-address of an interface {#Find out the mac-address of an interface}

-   `ip link`

#### How to get the ip-address of the interface `eth0`? {#How to get the ip-address of the interface eth0?}

-   `ip addr show dev eth0`

#### Turn networking interface on/off {#Turn networking interface on/off}

\> Have you tried to turning your device off and on again?

I case you do not get a ip-address

-   `ip link set eno1 down`
-   `ip link set eno1 up`

#### How to restrict access to a certain port? {#How to restrict access to a certain port?}

To directly restirct access, you would use the `iptables`-tool. With
this tool you can configure rules for network connection. Because this
tool itself is hard to handle (because of complexity), therefore there
is a wrapper-tool called `ufw` for the home user.

``` bash
# Drop everything accessing port 22
sudo iptables -A INPUT -p tcp --dport 22 -j DROP
# Accept <ip> on port 22
sudo iptables -A INPUT -p tcp --dport 22 -s <ip> -j ACCEPT
```

More about `iptables` on <https://www.netfilter.org/>

The successor of `iptables` is `nftables`.

#### Setting up a new interface {#Setting up a new interface}

Adding a new dummy interface for testing & simulation:

-   `ip link add dev eno2 type dummy`

#### Change the ip-address for an interface {#Change the ip-address for an interface}

-   Add a new one: `ip addr add 192.168.178.200/24 dev eno1`
-   Delete the old one: `ip addr del 192.168.178.104/24 dev eno1`

#### How to find out which network-manager is in use right now? {#How to find out which network-manager is in use right now?}

There is no other way than searching for all know managers.

-   `ps aux | grep -E 'NetworkManager|systemd-networkd|wpa_supplicant|connman|dhcpcd'`

### Advanced Topics {#Advanced Topics}

#### Filesystem {#Filesystem}

-   inodes
-   superblock
-   fsck
-   journaling

#### Memory {#Memory}

-   MMU
-   malloc(s)
-   page
-   memory allocation
-   life of an I/O

#### Processes {#Processes}

-   mutex/semaphore
-   deadlock/livelock
-   IPC (FIFO, fork, pipes signals)
-   file descriptor
-   context switching
-   scheduling
-   load balancing
