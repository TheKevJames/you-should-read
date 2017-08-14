-- Revert you-should-read:add_table_media from pg

BEGIN;

DROP TRIGGER update_media_timestamp ON ysr.media;

DROP TABLE ysr.media;

COMMIT;
