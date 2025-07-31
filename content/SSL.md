---
title: SSL
description: SSL means Secure Sockets Layer
---

## Check certificates
```bash
openssl s_client -connect mysite.de:443 -showcerts
```

## Fullchain

```
cat domain.cer intermediate.cer root.cer > fullchain.cer
```

## Test Certs

https://www.ssllabs.com/
