---
title: Wireguard
---

## TL;DR

- `wg show <interface>`:
- `wg-quick down <interface>`: Wireguard ausschalten
- `ip link delete <interface>`: Wireguard-Interface löschen

## Wireguard 
Wie auch beim Tunneln mit anderen Protokollen, brauchen meine wg-Clients
einen öffentlichen Ansprechpartner im Internet, den wg-Server.

Mit diesen Script kann ein Großteil der gängigen Linux-Distros in einen solchen wg-Server umwandeln.

- Installer-Script für den Server: https://github.com/angrisnttan/wireguard-install

Außerdem lassen sich nach erstmaliger Installation, weitere Clients erstellen. 
Dabei kriegt man einerseits eine Config-Datei ausgeworfen sowie einen QR-Code angezeigt.

Ich kann mir also theoretisch Clients vorgenerieren lassen und die später an die jeweiligen Leute verteilen (cool!).

## `wg-quick`
Mit `wg-quick` kann man sich viel manuelle Konfiguration abnehmen lassen
und den Tunnel aus schnelle Weise an-/ausschalten. Es werden root-Rechte benötigt.
Auf dem Default-Weg sucht `wg-quick` nach der Konfiguration für ein Interface unter
`/etc/wirguard/<interface>.conf`. Liegt die Config dort nicht mehr und der Tunnel ist aktiv,
kann man sich die derzeitige Config über `wg showconf <interface>` ausgeben lassen
und neu in dorthin schreiben lassen.

```bash
wg showconf <interface> > /etc/wireguard/<interface>.conf
```

### Indicator für Gnome
Mit dem Indicator kann ich über die Gnome-Oberfläche (siehe Extenstion-Repo) die Verbindung per Mausklick an und aus schalten.

- Extension für den Indicator: https://github.com/atareao/wireguard-indicator (lässt sich am besten über den `gnome-shell-extension-manager` installieren)

Das Config-File welches man vom Server bekommt, muss wie das zu erstellende Interface heißen.
```bash
mv my-laptop-wg0.conf wg0.conf
```
Dann kann man es per `nmcli` hinzufügen.
```bash
sudo nmcli connection import type wireguard file wg0.conf
```

Im Indicator sollte jetzt die Verbindung `wg0` angezeigt werden.

