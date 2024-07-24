# Vagrant 

Vagrant ermöglicht die Erstellung und Verwaltung von virtuellen
Maschinen.

## Kommandos 

-   `vagrant init`: erstellt in der derzeitigen Directory ein
    sogenanntes `Vagrantfile`
-   `vagrant status`: zeigt den Status der sogenannten Boxes (VMs) in
    der derzeitigen Directory
-   `vagrant global-status`: zeigt Status alles Boxes auf der
    Host-Maschine
-   `vagrant up`: Startet alle definierten Maschinen
-   `vagrant up <name>`: Startet mit `<name>` benannte Maschine

## Normaler Workflow 

## Virtualbox als Default-Provider 

Vagrant wählt zwischen Docker und VirtualBox als Backend/Provider für
die VMs. Setzt man diese Umgebungsvariable (z.B. in `~/.profile`) legt
mn VirtualBox fest.

``` bash
export VAGRANT_DEFAULT_PROVIDER=virtualbox
```

## `Vagrantfile` für Ubuntu-Maschine 

``` 
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"
  config.vm.network "private_network", ip: "192.168.56.10"
end
```