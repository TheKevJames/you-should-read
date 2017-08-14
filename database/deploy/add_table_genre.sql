-- Deploy you-should-read:add_table_genre to pg
-- requires: updated_at_fn

BEGIN;

CREATE TABLE ysr.genre (
    id          SERIAL      PRIMARY KEY,
    name        TEXT        NOT NULL,
    created_at  TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP   NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_genre_timestamp BEFORE UPDATE ON ysr.genre
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

COMMIT;
