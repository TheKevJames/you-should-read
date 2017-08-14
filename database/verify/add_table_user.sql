-- Verify you-should-read:add_table_user on pg

BEGIN;

SELECT id, name, created_at, updated_at
FROM ysr.user
WHERE FALSE;

SELECT 1 / COUNT(*)
FROM information_schema.triggers
WHERE trigger_name = 'update_user_timestamp';

ROLLBACK;
