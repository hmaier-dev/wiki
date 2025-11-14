---
categories:
- CI/CD
title: Ansible
---

-   `ansible-playbook -i inventory.ini add_admin_user.yml`

## Mit Vagrant 

Muss muss in der `inventory.ini` mit angeben, an welchem Ort sich der
Private-Key befindet. Sonst kann Ansible sich nicht mit der VM
verbinden.

``` ini
[test_machine]
192.168.56.10 ansible_ssh_user=vagrant ansible_ssh_private_key_file=.vagrant/machines/default/virtualbox/private_key
```

## `missing sudo password` 

Falls der Zieluser (`ansible_ssh_user`) auf dem System nicht root ist,
muss dieser in der `sudo`-Gruppe sein, als auch sein Password mitgegeben
werden. Dies tut man mit folgender Flag.

``` bash
ansible-playbook -i inventory.ini basic_setup.yml --ask-become-pass
```

## Setup
Zur Vorbereitung auf ein neues Projekt sollte man als erstes den Zugang via `ansible_user` testen.
Dafür deklariert man ein Inventory mit der IP-Adresse des Server sowie dem Namen des Users.
```ini
## inventory.ini
[all]
79.225.242.139 ansible_user=deploy
```
Damit kann man dann ein AdHoc-Ping ausführen.
```bash
ansible -i inventory.ini all -m ping
## [ERROR]: Task failed: Failed to connect to the host via ssh: deploy@79.225.242.139: Permission denied (publickey,password).
## Origin: <adhoc 'ping' task>
## 
## {'action': 'ping', 'args': {}, 'timeout': 0, 'async_val': 0, 'poll': 15}
## 
## 79.225.242.139 | UNREACHABLE! => {
##     "changed": false,
##     "msg": "Task failed: Failed to connect to the host via ssh: deploy@79.225.242.139: Permission denied (publickey,password).",
##     "unreachable": true
## }
```
Ansible versucht via SSH-Keys auf den Server zuzugreifen und schlägt fehl. Dies kann verschiedene Gründe haben, die mit einander zusammenhängen.

- User `deploy` wurde noch nicht angelegt
- Der Public-Key der lokalen Maschine wurde noch nicht auf dem Server eingepflegt

Dem kann man manuell (mit root-access) Abhilfe schaffen.
```bash
useradd deploy
mkdir -p /home/deploy
chown deploy:deploy /home/deploy
```
Zurück auf der lokalen Maschine kann man `ssh-copy-id` verwenden, was den lokalen Public-Key auf dem Server unter `/home/deploy/.ssh/authorized_keys` einpflegt.
```bash
ssh-copy-id deploy@79.225.242.139
```
Nun kann man nochmal ein AdHoc-Ping versuchen. 
```bash
ansible -i inventory.ini all -m ping
## 79.225.242.139 | SUCCESS => {
##     "ansible_facts": {
##         "discovered_interpreter_python": "/usr/bin/python3.11"
##     },
##     "changed": false,
##     "ping": "pong"
## }

```
