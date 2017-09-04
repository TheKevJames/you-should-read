-- Revert you-should-read:increase_rating_value_precision from pg

BEGIN;

ALTER TABLE ysr.recommendation ALTER COLUMN value TYPE NUMERIC(2,1);
ALTER TABLE ysr.rating ALTER COLUMN value TYPE NUMERIC(2,1);
ALTER TABLE ysr.media ALTER COLUMN rating TYPE NUMERIC(5,4);

COMMIT;
