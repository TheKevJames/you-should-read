-- Deploy you-should-read:add_table_rating to pg
-- requires: updated_at_fn
-- requires: add_table_media
-- requires: add_table_user

BEGIN;

CREATE TABLE ysr.rating (
    id          SERIAL          PRIMARY KEY,
    uid         INTEGER         NOT NULL REFERENCES ysr.user(id),
    mid         INTEGER         NOT NULL REFERENCES ysr.media(id),
    value       NUMERIC(2,1)    NOT NULL,
    created_at  TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_rating_timestamp BEFORE UPDATE ON ysr.rating
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

COMMIT;
