-- Verify you-should-read:updated_at_fn on pg

BEGIN;

SELECT pg_get_functiondef('update_timestamp()'::regprocedure);

ROLLBACK;
