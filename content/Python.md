---
title: Python
---

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


# List of URIs to check
uris = [
    URI(uri="https://www.example.com", want=200),
    URI(uri="https://www.nonexistentwebsite.com", want=404),
]
```
## Packaging a project

- https://packaging.python.org/en/latest/tutorials/packaging-projects/

