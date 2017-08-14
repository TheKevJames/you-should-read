-- Deploy you-should-read:add_table_bookmark to pg
-- requires: updated_at_fn
-- requires: add_table_media
-- requires: add_table_user

BEGIN;

CREATE TABLE ysr.bookmark (
    id          SERIAL          PRIMARY KEY,
    uid         INTEGER         NOT NULL REFERENCES ysr.user(id),
    mid         INTEGER         NOT NULL REFERENCES ysr.media(id),
    url         TEXT            NOT NULL,
    created_at  TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_bookmark_timestamp BEFORE UPDATE ON ysr.bookmark
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

COMMIT;
