-- Verify you-should-read:add_computed_value_columns on pg

BEGIN;

SELECT value_adjusted FROM ysr.rating;

ROLLBACK;
