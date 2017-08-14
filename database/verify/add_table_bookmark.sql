-- Verify you-should-read:add_table_bookmark on pg

BEGIN;

SELECT id, uid, mid, url, created_at, updated_at
FROM ysr.bookmark
WHERE FALSE;

SELECT 1 / COUNT(*)
FROM information_schema.triggers
WHERE trigger_name = 'update_bookmark_timestamp';

ROLLBACK;
