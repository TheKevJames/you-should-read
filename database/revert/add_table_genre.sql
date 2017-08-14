-- Revert you-should-read:add_table_genre from pg

BEGIN;

DROP TRIGGER update_genre_timestamp ON ysr.genre;

DROP TABLE ysr.genre;

COMMIT;
