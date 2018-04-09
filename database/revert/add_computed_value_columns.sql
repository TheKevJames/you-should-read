-- Revert you-should-read:add_computed_value_columns from pg

BEGIN;

ALTER TABLE ysr.rating DROP COLUMN value_adjusted;

COMMIT;
