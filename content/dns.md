---
title: DNS
---

## Special Domains

### `.local`
Be careful if you are using macOS or Linux machines in your network.
This domain is reserved for [mDNS](https://www.ip-insider.de/was-ist-mdns-a-c5bddb263411431b9cd036c6870b2789/),
which is like a plug-and-play DNS which doens't need a DNS server.

### `.dev`
In most browsers this domain is hardcoded t be used with [HSTS](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security). 
Don't use it for your local domain running HTTP.

## Brave Browser
If you locally configured DNS don't work, you need to configure the DNS-Provider.
By default it is OpenDNS. Under `brave://settings/security` you can set the OS-default
as the DNS. Now the browser takes the same DNS as the ethernet-interface.
