-- Deploy you-should-read:increase_rating_value_precision to pg
-- requires: add_table_media
-- requires: add_table_rating
-- requires: add_table_recommendation

BEGIN;

ALTER TABLE ysr.media ALTER COLUMN rating TYPE NUMERIC(6,4);
ALTER TABLE ysr.rating ALTER COLUMN value TYPE NUMERIC(3,1);
ALTER TABLE ysr.recommendation ALTER COLUMN value TYPE NUMERIC(3,1);

COMMIT;
