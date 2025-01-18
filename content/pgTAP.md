---
categories:
- databases
title: pgTAP
---

# Testing mit pgTAP

-   <https://pgtap.org/pg_prove.html>

## Pass if insertion fails 

``` sql
BEGIN; -- Test to check if the INSERT statement fails as expected
SELECT plan(1);


PREPARE status_insert AS INSERT INTO cmdb (name, beschreibung, status) VALUES ('foobar', 'barfoo', 'online');

-- Passes if code and message match the thrown error when 'status_insert' is executed
SELECT throws_ok(
    'status_insert',
    '23514', -- wanted error code https://www.postgresql.org/docs/current/errcodes-appendix.html
    'new row for relation "cmdb" violates check constraint "status_format"'); -- wanted shown message

SELECT * FROM finish();
ROLLBACK;
```
