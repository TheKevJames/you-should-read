-- Verify you-should-read:add_table_media_genre on pg

BEGIN;

SELECT id, mid, gid, created_at, updated_at
FROM ysr.media_genre
WHERE FALSE;

SELECT 1 / COUNT(*)
FROM information_schema.triggers
WHERE trigger_name = 'update_media_genre_timestamp';

ROLLBACK;
