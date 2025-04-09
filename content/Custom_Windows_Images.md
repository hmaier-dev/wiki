---
title: Custom Windows Images
description: How to make Windows more usable.
---
{{ $opts_sysprep := dict "/wiki" "/sysprep" }}
{{ $opts_dism := dict "/wiki" "/dism" }}

- {{ .Ref $opts_sysprep }}
- {{ .Ref $opts_dism }}
