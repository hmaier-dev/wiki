---
categories:
- databases
title: sqlite
---

## Dump data

```bash
sqlite3 sqlite-old.db .dump > backup.sql
```

## Insert dump
Keep in mind that `backup.sql` contains a `CREATE`-statement. If you want to just keep the data, delete the concerning lines.
```bash
# Linux
sqlite3 sqlite-new.db < backup.sql
# Windows
Get-Content backup.sql | sqlite3.exe sqlite.db
```
