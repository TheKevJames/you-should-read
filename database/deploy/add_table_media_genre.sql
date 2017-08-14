-- Deploy you-should-read:add_table_media_genre to pg
-- requires: updated_at_fn
-- requires: add_table_media
-- requires: add_table_genre

BEGIN;

CREATE TABLE ysr.media_genre (
    id          SERIAL      PRIMARY KEY,
    mid         INTEGER     NOT NULL REFERENCES ysr.media(id),
    gid         INTEGER     NOT NULL REFERENCES ysr.genre(id),
    created_at  TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP   NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_media_genre_timestamp BEFORE UPDATE ON ysr.media_genre
FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

COMMIT;
