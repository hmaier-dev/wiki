---
categories:
- coding
title: Python
description: No about snakes, but about a nice scripting language.
---

Is a nice scripting language in which you can easily build everything, with the trade-off of being slow.

## Virtual Environments


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

