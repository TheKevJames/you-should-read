-- Revert you-should-read:cascade_on_updates from pg

BEGIN;

-- ysr.recommendation
ALTER TABLE ysr.recommendation DROP CONSTRAINT recommendation_fuid_fkey;
ALTER TABLE ysr.recommendation ADD CONSTRAINT recommendation_fuid_fkey
    FOREIGN KEY (fuid) REFERENCES ysr.user(id);

ALTER TABLE ysr.recommendation DROP CONSTRAINT recommendation_tuid_fkey;
ALTER TABLE ysr.recommendation ADD CONSTRAINT recommendation_tuid_fkey
    FOREIGN KEY (tuid) REFERENCES ysr.user(id);

ALTER TABLE ysr.recommendation DROP CONSTRAINT recommendation_mid_fkey;
ALTER TABLE ysr.recommendation ADD CONSTRAINT recommendation_mid_fkey
    FOREIGN KEY (mid) REFERENCES ysr.media(id);

-- ysr.rating
ALTER TABLE ysr.rating DROP CONSTRAINT rating_uid_fkey;
ALTER TABLE ysr.rating ADD CONSTRAINT rating_uid_fkey
    FOREIGN KEY (uid) REFERENCES ysr.user(id);

ALTER TABLE ysr.rating DROP CONSTRAINT rating_mid_fkey;
ALTER TABLE ysr.rating ADD CONSTRAINT rating_mid_fkey
    FOREIGN KEY (mid) REFERENCES ysr.media(id);

-- ysr.media_genre
ALTER TABLE ysr.media_genre DROP CONSTRAINT media_genre_mid_fkey;
ALTER TABLE ysr.media_genre ADD CONSTRAINT media_genre_mid_fkey
    FOREIGN KEY (mid) REFERENCES ysr.media(id);

ALTER TABLE ysr.media_genre DROP CONSTRAINT media_genre_gid_fkey;
ALTER TABLE ysr.media_genre ADD CONSTRAINT media_genre_gid_fkey
    FOREIGN KEY (gid) REFERENCES ysr.genre(id);

-- ysr.bookmark
ALTER TABLE ysr.bookmark DROP CONSTRAINT bookmark_uid_fkey;
ALTER TABLE ysr.bookmark ADD CONSTRAINT bookmark_uid_fkey
    FOREIGN KEY (uid) REFERENCES ysr.user(id);

ALTER TABLE ysr.bookmark DROP CONSTRAINT bookmark_mid_fkey;
ALTER TABLE ysr.bookmark ADD CONSTRAINT bookmark_mid_fkey
    FOREIGN KEY (mid) REFERENCES ysr.media(id);

COMMIT;
