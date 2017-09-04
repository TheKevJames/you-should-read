-- Verify you-should-read:increase_rating_value_precision on pg

BEGIN;

-- for foreign keys
INSERT INTO ysr.user (id, name) VALUES (-1, 'user1'), (-2, 'user2');
INSERT INTO ysr.media (id, name) VALUES (-1, 'media1');

-- check ysr.media precision
INSERT INTO ysr.media (name, rating) VALUES ('test', 12.3456);

-- check ysr.rating precision
INSERT INTO ysr.rating (uid, mid, value) VALUES (-1, -1, 12.3);

-- check ysr.recommendation precision
INSERT INTO ysr.recommendation (fuid, tuid, mid, value) VALUES (-1, -2, -1, 12.3);

ROLLBACK;
