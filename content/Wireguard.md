---
title: Wireguard
---

# Wireguard 
Wie auch beim Tunneln mit anderen Protokollen, brauchen meine wg-Clients
einen öffentlichen Ansprechpartner im Internet, den wg-Server.

Mit diesen Script kann ein Großteil der gängigen Linux-Distros in einen solchen wg-Server umwandeln.

- Installer-Script für den Server: https://github.com/angrisnttan/wireguard-install

Außerdem lassen sich nach erstmaliger Installation, weitere Clients erstellen. 
Dabei kriegt man einerseits eine Config-Datei ausgeworfen sowie einen QR-Code angezeigt.

Ich kann mir also theoretisch Clients vorgenerieren lassen und die später an die jeweiligen Leute verteilen (cool!).

## Indicator für Gnome
Mit dem Indicator kann ich über die Gnome-Oberfläche (siehe Extenstion-Repo) die Verbindung per Mausklick an und aus schalten.

- Extension für den Indicator: https://github.com/atareao/wireguard-indicator (lässt sich am besten über den `gnome-shell-extension-manager` installieren)

Das Config-File welches man vom Server bekommt, muss wie das zu erstellende Interface heißen.
```bash
mv hp-laptop-hmaier-wg0.conf wg0.conf
```
Dann kann man es per `nmcli` hinzufügen.
```bash
sudo nmcli connection import type wireguard file wg0.conf
```

Im Indicator sollte jetzt die Verbindung `wg0` angezeigt werden.

