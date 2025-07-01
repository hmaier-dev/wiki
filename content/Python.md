---
categories:
- coding
title: Python
description: No about snakes, but about a nice scripting language.
---

Is a nice scripting language which enables you to easily _build everything_, with the trade-off of it being slow.

## Virtual Environments
Create a virtual environment in your current directory:
```bash
python -m venv .
```
You can install all kinds of packages with different version, without cluttering your host-system.

## Language Server Protocol
For Python coding in neovim I recommend **basedpyright**. It was the easiest to run.

Usually you would need npm to run pyright, but with basedpyright everything is compiled into on binaries you can execute.
Here is their Github: https://github.com/DetachHead/basedpyright and it is available over `:Mason`.

The basic LSP configuration looks like this:
```
require("lspconfig").basedpyright.setup({})
```

## I want to see the traceback 

``` python
import traceback
import sys

try:
    do_stuff()
except Exception:
    print(traceback.format_exc())
    # or
    print(sys.exc_info()[2])
```

## I want to have structs like in Go
For this you can use dataclasses. These convert a class by annotation into a dataclass.
```python
from dataclasses import dataclass

# Define a dataclass to hold the URIs and their expected status codes
@dataclass
class URI:
    uri: str
    want: int

test = URI(uri="https://www.nonexistentwebsite.com", want=404),
print(test.uri)
print(test.want)

```
## Packaging a project

- https://packaging.python.org/en/latest/tutorials/packaging-projects/

## Magic Packet
A magic packet is a frame which is send as broadcast into the network,
meant to start-up a computer which has Wake-On-LAN activated.
In most cases the WOL-option can be found in the BIOS.
The following script shows a function which takes any format of MAC-Address and broadcasts it to the network.
```python
#!/usr/bin/env python3
import socket
import struct

def wake_on_lan(mac_address):
    # Remove any separators from the MAC address and convert to bytes
    mac_bytes = bytes.fromhex(mac_address.replace(':', '').replace('-', ''))

    # Create the magic packet payload
    payload = b'\xff' * 6 + mac_bytes * 16

    # Set up the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Send the magic packet to the broadcast address on port 9
    sock.sendto(payload, ('<broadcast>', 9))
    sock.close()

mac_address = 'F2:1F:AF:30:9F:10'  # Replace with the target MAC address
wake_on_lan(mac_address)
```


