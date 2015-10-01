DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    id_social         TEXT UNIQUE NOT NULL,
    name              TEXT NOT NULL,
    email             TEXT,
    image_url         TEXT,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS media;
CREATE TABLE media (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    title             TEXT UNIQUE NOT NULL,
    author            TEXT,
    link              TEXT NOT NULL,
    description       TEXT,
    length            INTEGER NOT NULL,
    rating_bayesian   REAL NOT NULL DEFAULT 0.0,
    rating_average    REAL NOT NULL DEFAULT 0.0,
    user_id           INTEGER NOT NULL REFERENCES user (id),
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS rating;
CREATE TABLE rating (
    user_id           INTEGER NOT NULL REFERENCES user (id),
    media_id          INTEGER NOT NULL REFERENCES media (id),
    value             INTEGER NOT NULL,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, media_id)
);

DROP TABLE IF EXISTS recommendation;
CREATE TABLE recommendation (
    from_user_id      INTEGER NOT NULL REFERENCES user (id),
    to_user_id        INTEGER NOT NULL REFERENCES user (id),
    media_id          INTEGER NOT NULL REFERENCES media (id),
    value             INTEGER NOT NULL,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (from_user_id, to_user_id, media_id)
);

DROP TABLE IF EXISTS status;
CREATE TABLE status (
    user_id           INTEGER NOT NULL REFERENCES user (id),
    media_id          INTEGER NOT NULL REFERENCES media (id),
    value             INTEGER NOT NULL,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, media_id)
);
