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
