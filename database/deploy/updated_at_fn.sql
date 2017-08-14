-- Deploy you-should-read:updated_at_fn to pg
-- requires: appschema

BEGIN;

CREATE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

COMMIT;
