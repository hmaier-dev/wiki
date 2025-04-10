---
title: Custom Windows Images
description: How to make Windows more usable.
---
Beim Bereitstellen von multiplen Maschinen mit Windows-Betriebssytem, wird man beim Durchleben von hohem zeitlichen Aufwand und der
damit einhergehenden Lethargie, irgendwann anfangen nach Automatisierungs-Möglichkeiten zu forschen.
Mit modifizierten Windows-Images kann man sich widerkehrende Installationsroutinen und Konfigurationen ersparen, und somit der Lethargie enfliehen.

## TL;DR (too long; didn't read)
1. Rechner mit jeglicher Software ausstatten
2. Abbild des gesamten Systems erfassen
3. System-Abbild auf weiteren Rechnern installieren

## Anleitung
Falls im Folgenden Fehler auftreten, habe ich meine Erfahrungen in diesen Artikeln dokumentiert.

- [sysprep]({{% ref path="sysprep" %}})
- [dism]({{% ref path="dism" %}})
- [oscdimg]({{% ref path="oscdimg" %}})

## `autounattend.xml`
Um Einstellungen bei der Installation vorzudefinieren, kann man sich eine Antwortdatei bauen. Diese kann zum Beispiel `autounattend.xml` heißen. Diese muss mit in der ISO liegen; also im Ordner bevor man mit `oscdimg` die ISO erstellt.
Hat man die standard Windows ISO auf `C:\` exthrahiert, muss die `autounattend.xml` hier liegen: `C:\Win10_22H2_German_x64v1\autounattend.xml`.
Zur Kontrolle der Antwortdatei ist der _Windows System Image Manager_ (SIM) hilfreich, welchen man sich aus der ADK erstellen kann.

## FAQ

- Wie kommt man in die `cmd` während der Installation?
    - `SHIFT+F10`
