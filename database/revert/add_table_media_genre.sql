-- Revert you-should-read:add_table_media_genre from pg

BEGIN;

DROP TRIGGER update_media_genre_timestamp ON ysr.media_genre;

DROP TABLE ysr.media_genre;

COMMIT;
