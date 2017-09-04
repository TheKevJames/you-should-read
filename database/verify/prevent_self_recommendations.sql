-- Verify you-should-read:prevent_self_recommendations on pg

BEGIN;

-- for foreign keys
INSERT INTO ysr.user (id, name) VALUES (-1, 'user1'), (-2, 'user2');
INSERT INTO ysr.media (id, name) VALUES (-1, 'media1');

-- ensure exception is not thrown
INSERT INTO ysr.recommendation (fuid, tuid, mid, value) VALUES (-1, -2, -1, 3.2);

ROLLBACK;
