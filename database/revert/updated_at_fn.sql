-- Revert you-should-read:updated_at_fn from pg

BEGIN;

DROP FUNCTION update_timestamp();

COMMIT;
