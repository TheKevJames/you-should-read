-- Verify you-should-read:add_table_recommendation on pg

BEGIN;

SELECT id, fuid, tuid, mid, value, created_at, updated_at
FROM ysr.recommendation
WHERE FALSE;

SELECT 1 / COUNT(*)
FROM information_schema.triggers
WHERE trigger_name = 'update_recommendation_timestamp';

ROLLBACK;
