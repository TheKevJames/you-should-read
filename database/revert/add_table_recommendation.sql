-- Revert you-should-read:add_table_recommendation from pg

BEGIN;

DROP TRIGGER update_recommendation_timestamp ON ysr.recommendation;

DROP TABLE ysr.recommendation;

COMMIT;
