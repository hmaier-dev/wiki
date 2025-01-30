---
categories:
- coding
- editors 
title: lua
---

The most important software from Brasil.

# Printing tables to the console 

Found on
<https://stackoverflow.com/questions/9168058/how-to-dump-a-table-to-console>

``` lua
function dump(o)
   if type(o) == 'table' then
      local s = '{ '
      for k,v in pairs(o) do
         if type(k) ~= 'number' then k = '"'..k..'"' end
         s = s .. '['..k..'] = ' .. dump(v) .. ','
      end
      return s .. '} '
   else
      return tostring(o)
   end
end

#### ODER

local inspect = require('inspect') # externe lib
print(inspect(out))

```
