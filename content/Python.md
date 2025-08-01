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

## LDAP Query
This examples uses the current Kerberos ticket to auth to the ldap server.
In most cases this will just work in Windows.
```python
# pip install -r requirements.txt

# ldap3==2.9.1
# pyasn1==0.6.1
# winkerberos==0.12.2
import winkerberos as k
from ldap3 import Server, Connection, SASL, GSSAPI, SUBTREE
from dataclasses import dataclass
from typing import Any, List


# Use current users kerberos ticket.
# See all active tickets with `klist`.
def auth_kerberos(service_principal):
    print(f"\nAttempting Kerberos authentication for SPN: {service_principal}")
    try:
        status, ctx = k.authGSSClientInit(service_principal)
        if status != k.AUTH_GSS_COMPLETE and status != k.AUTH_GSS_CONTINUE:
            return False, f"Failed to initialize GSSAPI context: {status}"
        client_token = ""
        while status == k.AUTH_GSS_CONTINUE:
            print("Current GSSAPI status: AUTH_GSS_CONTINUE")
            status = k.authGSSClientStep(ctx, client_token)
            response_token = k.authGSSClientResponse(ctx)
            if response_token is None:
                if status == k.AUTH_GSS_COMPLETE:
                    print("GSSAPI authentication complete, no more client response needed.")
                    break
                else:
                    return False, "GSSAPI step produced no response token."
        print("GSSAPI authentication complete.")
        return True, "Authentication complete."
    except k.GSSError as e:
        # This catches errors during the GSSAPI negotiation
        error_message = f"Kerberos GSSAPI Error: {e}"
        print(error_message)
        return False, error_message
    except Exception as e:
        # Catch other unexpected errors
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return False, error_message
# End Kerberos Auth


ATTRIBUTES = [
    'distinguishedName',
    'mail',
    'mailNickname']

def browse(host, ous):
    print(f"Connecting to LDAP server: {host}")
    server = Server(host, use_ssl=False)  # Change use_ssl=True if needed
    # SASL GSSAPI = use current Kerberos ticket
    conn = Connection(
        server,
        authentication=SASL,
        sasl_mechanism=GSSAPI,
        auto_bind=True,
        read_only=True
    )
    print("LDAP bind successful.")
    for ou in ous:
        cookie = b''
        while True:
            conn.search(
                search_base=ou,
                search_filter='(objectClass=user)',
                search_scope=SUBTREE,
                attributes=ATTRIBUTES,
                paged_size=1000,
                paged_cookie=cookie
            )
            read_page(conn)
            ## If Cookie is set, pull another page
            cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
            if not cookie:
                break
    conn.unbind()

## There is a restriction for the amount of entries returned by a ldap-request
def read_page(conn: Connection):
    for entry in conn.entries:
        for a in ATTRIBUTES:
            print(entry[a].values)


# MAIN
SERVICE_SPN = ""
LDAP_HOST = ""
OUs = [
  "OU=IT,OU=Users,DC=company,DC=de",
]
success, result = auth_kerberos(SERVICE_SPN)
print(success, result)
browse(LDAP_HOST, OUs)
```

## Pandas
Pandas sind nicht nur toll, sondern helfen auch zur Datenanalyse. Folgendes Beispiel: Ich habe zwei csv-Dateien in den ich jeweils einen Key habe.
Nun möchte ich die Einträgen zusammenführen, in denen in beiden Dateien der Key gleich ist. Mithilfe des Pakets `pandas` kann ich dafür einen _Inner Join_ verwenden.
```python
import pandas as pd

bestellcenter_path = r".\bestellcenter-sim-numbers.csv"
mdm_path = r".\mdm-data.csv"

bc_df = pd.read_csv(bestellcenter_path, encoding="cp1252", sep=";", dtype={"SIM-Nummer": str})
mdm_df = pd.read_csv(mdm_path, encoding="cp1252", sep=",", dtype={"SIM Karten Seriennummer": str})

print(bc_df)
print(mdm_df)

mdm_df["SIM Karten Seriennummer"] = (
    mdm_df["SIM Karten Seriennummer"].astype(str).str[6:]
)

## Bestellcenter key
col1 = "SIM-Nummer"
## MDM Key
col2 = "SIM Karten Seriennummer"

# Ein Inner Join nimmt nur die Rows in denen der Key in beiden Datenframes gleich ist
merged_df = pd.merge(bc_df, mdm_df, left_on=col1, right_on=col2, how="inner")

# '~' is hier ein logischer NOT operator
# Hole mir alle MDM Einträge die nicht im Bestellcenter sind
not_matched_df = mdm_df[~mdm_df[col2].isin(bc_df[col1])]

print("SIM Karten, die im MDM und im Bestellcenter sind")
print(merged_df)

print("SIM Karten, die nicht im Bestellcenter gefunden wurden: ")
print(not_matched_df)

```


