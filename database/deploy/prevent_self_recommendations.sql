-- Deploy you-should-read:prevent_self_recommendations to pg
-- requires: add_table_recommendation

BEGIN;

ALTER TABLE ysr.recommendation
ADD CONSTRAINT fuid_cannot_be_equal_to_tuid
CHECK (fuid <> tuid);

COMMIT;
