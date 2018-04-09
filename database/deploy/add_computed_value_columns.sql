-- Deploy you-should-read:add_computed_value_columns to pg
-- requires: add_table_rating

BEGIN;

ALTER TABLE ysr.rating ADD COLUMN value_adjusted NUMERIC(5,3) NOT NULL DEFAULT 0;

COMMIT;
