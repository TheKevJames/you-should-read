-- Revert you-should-read:add_table_bookmark from pg

BEGIN;

DROP TRIGGER update_bookmark_timestamp ON ysr.bookmark;

DROP TABLE ysr.bookmark;

COMMIT;
