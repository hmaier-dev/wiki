---
categories:
- databases
title: Goose
description: Not about birds, but about a tool for database-migrations.
---

# Goose 

Ist ein gutes Tool für Datenbank-Migrationen. Damit ist möglich
inkrementell `sql`-Files einzuspielen. Verschiedenen Migrationen bauen
also aufeinander auf. Mit Goose bildet man also die Evolution seiner
Datenbank ab. Es ist möglich mit `up` und `down` zwischen den
verschiedenen Evolutionsstufen zu switchen.

# Normaler Use-Case 

``` bash
export DB_URL=postgres://postgres:password@172.17.0.3:5432/cmdb
goose -allow-missing -dir ./migrations postgres $DB_URL up

## Wie sieht es in ./migrations aus?
## z.b. so:
# .
# ├── 00001_audit_log.sql
# ├── 00002_cmdb.sql
# ├── 00003_cables.sql
# ├── 00004_domains.sql
# ├── 00005_office.sql
# ├── 20230119114311_cmdb_add_mac_addresses.sql
# ├── 20230119160151_add_all_ips_view.sql
# ├── 20230202173045_add_comments.sql
# ├── 20230208194650_create_table_registered_domains.sql
# ├── 20230316165343_cmdb_v2_add_mac_addresses.sql
# ├── 20230320150211_cables_add_unique_constraints.sql
# ├── 20230321100754_audit_table.sql
# ├── 20230324171716_add_cables_references.sql
# ├── 20230327134036_add_vm_spec_checks.sql
# ├── 20230404161325_audit_search_path.sql
# ├── 20230511123022_cables_v1_view.sql
# ├── 20230523131012_add_shared_ip_type.sql
# ├── 20230920143845_add_datacenter_ntt_ber1.sql
# ├── 20240207104924_extract_location_functions.sql
# ├── 20240207144735_create_table_cloud_machines.sql
# ├── 20240207154335_cloud_is_label.sql
# └── 20240318172042_add_cloud_contract_columns.sql
```

# Migration schreiben 

Dies ist eine Evolutionsstufe. Es wird definiert wie man, die Stufe
erreicht (`+goose Up`) und wie man die Änderungen wieder rückgängig
(`+goose Down`) macht.

``` sql
-- +goose Up
-- +goose StatementBegin
ALTER TABLE cmdb DROP CONSTRAINT status_format;
ALTER TABLE cmdb ADD CONSTRAINT status_format CHECK (((status)::text ~* '^(online:.*|online:.*/.*|offline|security|ignore)$'::text));
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
ALTER TABLE cmdb DROP CONSTRAINT status_format;
ALTER TABLE cmdb ADD CONSTRAINT status_format CHECK (((status)::text ~* '^(online|online:.*|online:.*/.*|offline|security|ignore)$'::text));
-- +goose StatementEnd
```
