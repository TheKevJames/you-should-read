-- Deploy you-should-read:cascade_on_updates to pg
-- requires: add_table_bookmark
-- requires: add_table_media_genre
-- requires: add_table_rating
-- requires: add_table_recommendation

BEGIN;

-- ysr.bookmark
ALTER TABLE ysr.bookmark DROP CONSTRAINT bookmark_uid_fkey;
ALTER TABLE ysr.bookmark ADD CONSTRAINT bookmark_uid_fkey
    FOREIGN KEY (uid) REFERENCES ysr.user(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ysr.bookmark DROP CONSTRAINT bookmark_mid_fkey;
ALTER TABLE ysr.bookmark ADD CONSTRAINT bookmark_mid_fkey
    FOREIGN KEY (mid) REFERENCES ysr.media(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

-- ysr.media_genre
ALTER TABLE ysr.media_genre DROP CONSTRAINT media_genre_mid_fkey;
ALTER TABLE ysr.media_genre ADD CONSTRAINT media_genre_mid_fkey
    FOREIGN KEY (mid) REFERENCES ysr.media(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ysr.media_genre DROP CONSTRAINT media_genre_gid_fkey;
ALTER TABLE ysr.media_genre ADD CONSTRAINT media_genre_gid_fkey
    FOREIGN KEY (gid) REFERENCES ysr.genre(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

-- ysr.rating
ALTER TABLE ysr.rating DROP CONSTRAINT rating_uid_fkey;
ALTER TABLE ysr.rating ADD CONSTRAINT rating_uid_fkey
    FOREIGN KEY (uid) REFERENCES ysr.user(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ysr.rating DROP CONSTRAINT rating_mid_fkey;
ALTER TABLE ysr.rating ADD CONSTRAINT rating_mid_fkey
    FOREIGN KEY (mid) REFERENCES ysr.media(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

-- ysr.recommendation
ALTER TABLE ysr.recommendation DROP CONSTRAINT recommendation_fuid_fkey;
ALTER TABLE ysr.recommendation ADD CONSTRAINT recommendation_fuid_fkey
    FOREIGN KEY (fuid) REFERENCES ysr.user(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ysr.recommendation DROP CONSTRAINT recommendation_tuid_fkey;
ALTER TABLE ysr.recommendation ADD CONSTRAINT recommendation_tuid_fkey
    FOREIGN KEY (tuid) REFERENCES ysr.user(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ysr.recommendation DROP CONSTRAINT recommendation_mid_fkey;
ALTER TABLE ysr.recommendation ADD CONSTRAINT recommendation_mid_fkey
    FOREIGN KEY (mid) REFERENCES ysr.media(id)
    ON UPDATE CASCADE ON DELETE CASCADE;

COMMIT;
