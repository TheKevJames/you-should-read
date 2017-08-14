-- Verify you-should-read:appschema on pg

BEGIN;

SELECT pg_catalog.has_schema_privilege('ysr', 'usage');

ROLLBACK;
