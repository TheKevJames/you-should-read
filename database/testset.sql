BEGIN;

DELETE FROM ysr.user;
INSERT INTO ysr.user (id, name) VALUES
    (1, 'Ginelle'),
    (2, 'Harvey'),
    (3, 'Kevin'),
    (4, 'Lara'),
    (5, 'Tyler');
DELETE FROM ysr.media;
INSERT INTO ysr.media (id, name, url) VALUES
    (1, 'Worm', 'https://parahumans.wordpress.com/category/stories-arcs-1-10/arc-1-gestation/1-01/'),
    (2, 'Skulduggery Pleasant', NULL),
    (3, 'Benefactor', 'https://forums.spacebattles.com/threads/benefactor-one-off-original-superhero-fiction.342377/'),
    (4, 'Demon', 'http://www.shigabooks.com/index.php?page=001'),
    (5, 'HPMOR', 'http://hpmor.com/chapter/1'),
    (6, 'The Belgariad', NULL),
    (7, 'Vorkosigan Saga', NULL),
    (8, 'The Gamer', 'http://mangafox.me/manga/the_gamer/c001/1.html'),
    (9, 'Mistborn', NULL),
    (10, 'MythAdventures', NULL),
    (11, 'Poison Study Series', NULL),
    (12, 'Luminosity', 'http://luminous.elcenia.com/'),
    (13, 'Tower of God', 'http://mangafox.me/manga/tower_of_god/'),
    (14, 'Kubera', 'http://mangafox.me/manga/kubera/'),
    (15, 'Shokugenki No Soma', 'http://mangafox.me/manga/shokugeki_no_soma/'),
    (16, 'Dresden Files', NULL),
    (17, 'Lackadaisy', 'http://www.lackadaisycats.com/'),
    (18, 'Transfer Student Storm Bringer', 'http://mangafox.me/manga/transfer_student_storm_bringer/'),
    (19, 'Pact', ' https://pactwebserial.wordpress.com/2013/12/17/bonds-1-1/'),
    (20, 'The Last Christmas', 'https://www.fanfiction.net/s/9915682/1/The-Last-Christmas'),
    (21, 'Charon', 'https://www.fanfiction.net/s/10570176/1/Charon'),
    (22, 'Record of Fallen Vampire', 'http://www.mangahere.co/manga/the_record_of_fallen_vampire/'),
    (23, 'Suicide Island', 'http://mangafox.me/manga/suicide_island/'),
    (24, 'Nimona', 'http://gingerhaze.com/nimona/comic/page-1'),
    (25, 'Be Heun', 'http://mangafox.me/manga/be_heun'),
    (26, 'HP and the Natural 20', 'https://www.fanfiction.net/s/8096183/1/Harry-Potter-and-the-Natural-20'),
    (27, 'Gunnerkrigg Court', 'http://www.gunnerkrigg.com/?p=1'),
    (28, 'Bookhunter', 'http://www.shigabooks.com/bookhunter.php'),
    (29, 'Fleep', 'http://www.shigabooks.com/fleep.php'),
    (30, 'Assasination Classroom', 'http://mangafox.me/manga/ansatsu_kyoushitsu/'),
    (31, 'The Two Year Emperor', 'https://www.fanfiction.net/s/9669819/1/The-Two-Year-Emperor'),
    (32, 'Time Braid', 'https://www.fanfiction.net/s/5193644/1/Time-Braid'),
    (33, 'The Practice Effect', NULL),
    (34, 'What if Drone Warfare had Come First?', 'https://squid314.livejournal.com/338607.html'),
    (35, 'God of High School', 'http://mangafox.me/manga/the_god_of_high_school/'),
    (36, 'Artie', 'https://www.fictionpress.com/s/3223802/1/Artie'),
    (37, 'Beelzebub', 'http://mangafox.me/manga/beelzebub/'),
    (38, 'The Breaker', 'http://mangafox.me/manga/the_breaker/'),
    (39, 'Arachnid', 'http://mangafox.me/manga/arachnid/'),
    (40, 'Oh, My God!', 'http://mangafox.me/manga/oh_my_god/'),
    (41, 'To the Stars', 'https://www.fanfiction.net/s/7406866/1/To-the-Stars'),
    (42, 'Log Horizon', 'http://mangafox.me/manga/log_horizon/'),
    (43, 'Floornight', 'http://archiveofourown.org/works/2372021/chapters/5238359'),
    (44, 'Denpa Kyoushi', 'http://mangafox.me/manga/denpa_kyoushi'),
    (45, 'Saga of Soul', 'http://www.sagaofsoul.com/story.html'),
    (46, 'Applied Cultural Anthology', 'https://www.fanfiction.net/s/9238861/1/Applied-Cultural-Anthropology-or'),
    (47, 'Ava''s Demon', 'http://www.avasdemon.com/pages.php#0001'),
    (48, 'Waves Arisen', 'https://wertifloke.wordpress.com/2015/01/25/chapter-1/'),
    (49, 'Pokemon: Origin of Species', 'https://www.fanfiction.net/s/9794740/1/Pokemon-The-Origin-of-Species'),
    (50, 'Twig', 'https://twigserial.wordpress.com/'),
    (51, 'The Games We Play', 'https://forums.spacebattles.com/threads/the-games-we-play-rwby-the-gamer-ryuugi-complete.351105/'),
    (52, 'Zombie Knight', 'http://thezombieknight.blogspot.ca/p/blog-page_19.html'),
    (53, 'Murasakiiro No Qualia', 'http://mangafox.me/manga/murasakiiro_no_qualia/'),
    (54, 'Coding Machines', 'http://www.teamten.com/lawrence/writings/coding-machines/'),
    (55, 'Team Anko', 'https://www.fanfiction.net/s/11087425/1/Team-Anko'),
    (56, 'Symbiote', 'https://farmerbob1.wordpress.com/2013/11/13/chapter-1-a-meeting-of-the-minds/'),
    (57, 'Free Radical', 'http://www.shamusyoung.com/shocked/main.php'),
    (58, 'Shadows of the Limelight', 'http://alexanderwales.com/shadows-of-the-limelight-ch-1-the-rooftop-races/'),
    (59, 'Triangle Opportunity', 'https://www.inkitt.com/stories/horror/7465'),
    (60, 'Toni Stark', 'http://archiveofourown.org/series/347126'),
    (61, 'Cordyceps', 'http://archiveofourown.org/works/6178036/chapters/14154868');
DELETE FROM ysr.rating;
INSERT INTO ysr.rating (uid, mid, value) VALUES
    -- ginelle
    (1, 5, 9),
    (1, 7, 9),
    (1, 8, 8),
    (1, 9, 9),
    (1, 11, 8),
    (1, 12, 8),
    (1, 13, 8),
    (1, 22, 7),
    (1, 23, 7),
    (1, 30, 10),
    (1, 42, 5),
    (1, 49, 4),
    -- harvey
    (2, 1, 10),
    (2, 5, 8),
    (2, 6, 8),
    (2, 7, 9),
    (2, 9, 8),
    (2, 16, 7),
    (2, 26, 7),
    -- kevin
    (3, 1, 10),
    (3, 2, 9),
    (3, 3, 9),
    (3, 4, 9),
    (3, 5, 10),
    (3, 6, 9),
    (3, 7, 7),
    (3, 8, 6),
    (3, 9, 9),
    (3, 12, 8),
    (3, 16, 8),
    (3, 17, 7),
    (3, 18, 8),
    (3, 19, 7),
    (3, 20, 7),
    (3, 21, 7),
    (3, 24, 7),
    (3, 26, 7),
    (3, 27, 7),
    (3, 28, 7),
    (3, 29, 9),
    (3, 30, 3),
    (3, 31, 6),
    (3, 32, 6),
    (3, 33, 6),
    (3, 34, 6),
    (3, 36, 6),
    (3, 40, 3),
    (3, 41, 5),
    (3, 43, 5),
    (3, 45, 5),
    (3, 46, 4),
    (3, 47, 4),
    (3, 48, 4),
    (3, 49, 7),
    (3, 51, 8),
    (3, 53, 6),
    (3, 54, 8),
    (3, 55, 7),
    (3, 56, 9),
    (3, 57, 9),
    (3, 58, 9),
    (3, 59, 8),
    (3, 60, 7),
    (3, 61, 9),
    -- lara
    (4, 1, 10),
    (4, 2, 10),
    (4, 5, 9),
    (4, 8, 9),
    (4, 9, 9),
    (4, 10, 8),
    (4, 13, 8),
    (4, 14, 8),
    (4, 15, 8),
    (4, 16, 8),
    (4, 17, 8),
    (4, 18, 7),
    (4, 25, 7),
    (4, 27, 7),
    (4, 35, 6),
    (4, 37, 6),
    (4, 38, 6),
    (4, 39, 6),
    (4, 40, 8),
    (4, 44, 5),
    -- tyler
    (5, 1, 9),
    (5, 5, 8),
    (5, 8, 9),
    (5, 15, 8);


COMMIT;
