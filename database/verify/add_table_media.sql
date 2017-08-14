-- Verify you-should-read:add_table_media on pg

BEGIN;

SELECT id, name, url, rating, created_at, updated_at
FROM ysr.media
WHERE FALSE;

SELECT 1 / COUNT(*)
FROM information_schema.triggers
WHERE trigger_name = 'update_media_timestamp';

ROLLBACK;
