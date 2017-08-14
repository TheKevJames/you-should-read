-- Deploy you-should-read:add_table_user to pg
-- requires: updated_at_fn

BEGIN;

CREATE TABLE ysr.user (
    id          SERIAL      PRIMARY KEY,
    name        TEXT        NOT NULL,
    created_at  TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP   NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_user_timestamp BEFORE UPDATE ON ysr.user
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

COMMIT;
