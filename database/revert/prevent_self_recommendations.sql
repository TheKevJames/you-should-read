-- Revert you-should-read:prevent_self_recommendations from pg

BEGIN;

ALTER TABLE ysr.recommendation
DROP CONSTRAINT fuid_cannot_be_equal_to_tuid;

COMMIT;
