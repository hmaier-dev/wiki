---
title: Pihole
description: DNS Sinkhole to block annoying ads
---

## Local DNS Records
Unter `System > Settings > Local DNS Records` kann man lokale DNS Records pflegen.
Es lassen sich sowohl A-Records als auch CNAME Records pflegen.

Hat man das Pihole am Router als DNS-Server eingetragen, kann es trotz korrekter Konfiguration sein,
dass der Router DNS-Antworten, die auf IP-Adressen im eigenen Netzwerk verweisen, blockiert.
Das kann sein, da auf dem Router der **DNS-Rebind-Schutz** aktiviert ist.
Diesen zu deaktivieren ist in den meisten Fällen keine gute Idee. Allerdings kann man Ausnahmen für Domains angeben,
die im eigenen Netzwerk verfügbar sind.

Die Einstellung findet man unter `Netzwerk > Netzwerkeinstellungen > DNS-Rebind-Schutz`.
