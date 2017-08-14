-- Revert you-should-read:appschema from pg

BEGIN;

DROP SCHEMA ysr;

COMMIT;
