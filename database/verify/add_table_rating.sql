-- Verify you-should-read:add_table_rating on pg

BEGIN;

SELECT id, uid, mid, value, created_at, updated_at
FROM ysr.rating
WHERE FALSE;

SELECT 1 / COUNT(*)
FROM information_schema.triggers
WHERE trigger_name = 'update_rating_timestamp';

ROLLBACK;
