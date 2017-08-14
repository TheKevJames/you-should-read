-- Revert you-should-read:add_table_user from pg

BEGIN;

DROP TRIGGER update_user_timestamp ON ysr.user;

DROP TABLE ysr.user;

COMMIT;
