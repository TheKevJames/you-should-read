-- Deploy you-should-read:add_table_media to pg
-- requires: updated_at_fn

BEGIN;

CREATE TABLE ysr.media (
    id          SERIAL          PRIMARY KEY,
    name        TEXT            NOT NULL,
    url         TEXT,
    rating      NUMERIC(5,4)    NOT NULL DEFAULT 0,
    created_at  TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_media_timestamp BEFORE UPDATE ON ysr.media
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

COMMIT;
