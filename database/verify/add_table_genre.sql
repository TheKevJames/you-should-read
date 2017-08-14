-- Verify you-should-read:add_table_genre on pg

BEGIN;

SELECT id, name, created_at, updated_at
FROM ysr.genre
WHERE FALSE;

SELECT 1 / COUNT(*)
FROM information_schema.triggers
WHERE trigger_name = 'update_genre_timestamp';

ROLLBACK;
