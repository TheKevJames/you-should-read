-- Revert you-should-read:add_table_rating from pg

BEGIN;

DROP TRIGGER update_rating_timestamp ON ysr.rating;

DROP TABLE ysr.rating;

COMMIT;
