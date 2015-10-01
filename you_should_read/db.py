import logging


logger = logging.getLogger(__name__)


def add_media(conn, title, author, link, description, length, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """ INSERT INTO media
                    (title, author, link, description, length, user_id)
                VALUES (?, ?, ?, ?, ?, ?) """, (title, author, link,
                                                description, length, user_id))
        conn.commit()

        return cursor.lastrowid
    except Exception as e:
        logger.error('add_media: caught exception')
        logger.exception(e)
        return -1


def add_user(conn, social_id, name, email, image_url):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """ INSERT INTO user (id_social, name, email, image_url)
                VALUES (?, ?, ?, ?) """, (social_id, name, email, image_url))
        conn.commit()

        return cursor.lastrowid
    except Exception as e:
        logger.error('add_user: caught exception')
        logger.exception(e)
        return -1


def get_media(conn, user_id, media_id=None, title=None):
    try:
        if media_id:
            cur = conn.cursor().execute(
                """ SELECT m.id, m.title, m.author, m.link, m.description,
                           m.length, m.rating_bayesian, u.name,
                           COALESCE(rt.value, 0)
                    FROM media m
                    INNER JOIN user u ON m.user_id = u.id
                    LEFT JOIN rating rt ON rt.user_id = ?
                        AND rt.media_id = m.id
                    WHERE m.id = ? """, (user_id, media_id))
        elif title:
            cur = conn.cursor().execute(
                """ SELECT m.id, m.title, m.author, m.link, m.description,
                           m.length, m.rating_bayesian, u.name,
                           COALESCE(rt.value, 0)
                    FROM media m
                    INNER JOIN user u ON m.user_id = u.id
                    LEFT JOIN rating rt ON rt.user_id = ?
                        AND rt.media_id = m.id
                    WHERE m.title = ? """, (user_id, title))
        else:
            raise Exception('tried to search by unsupported field')

        row = cur.fetchone()
        return dict(id=row[0], title=row[1], author=row[2], link=row[3],
                    description=row[4], length=row[5], rating=row[6],
                    username=row[7], personal_rating=row[8])
    except Exception as e:
        logger.error('get_media: caught exception')
        logger.exception(e)
        return dict()


def get_media_ids(conn):
    try:
        cur = conn.cursor().execute('SELECT id FROM media')

        return [x[0] for x in cur.fetchall()]
    except Exception as e:
        logger.error('get_media_ids: caught exception')
        logger.exception(e)
        return list()


def get_media_rating_average(conn, media_id=None):
    try:
        if media_id:
            cur = conn.cursor().execute(
                """ SELECT rating_average
                    FROM media
                    WHERE id = ? """, (media_id, ))
        else:
            cur = conn.cursor().execute(
                """ SELECT SUM(rating_average) / COUNT(*)
                    FROM media """)

        return cur.fetchone()[0]
    except Exception as e:
        logger.error('get_media_rating_average: caught exception')
        logger.exception(e)
        return 0


def get_media_rating_count(conn, media_id=None):
    try:
        if media_id:
            cur = conn.cursor().execute(
                """ SELECT COUNT(*)
                    FROM rating
                    WHERE media_id = ? """, (media_id, ))

            return cur.fetchone()[0]
        else:
            cur = conn.cursor().execute(
                """ SELECT COUNT(*)
                    FROM rating
                    GROUP BY media_id """)

            return [x[0] for x in cur.fetchall()]
    except Exception as e:
        logger.error('get_media_rating_count: caught exception')
        logger.exception(e)
        return list()


def get_ratings(conn, media_id):
    try:
        cur = conn.cursor().execute(
            """ SELECT value
                FROM rating
                WHERE media_id = ? """, (media_id, ))

        return [x[0] for x in cur.fetchall()]
    except Exception as e:
        logger.error('get_ratings: caught exception')
        logger.exception(e)
        return list()


def get_recommended(conn, user_id, include_read=False, limit=5):
    try:
        if include_read:
            cur = conn.cursor().execute(
                """ SELECT m.id, m.title, m.author, m.description, m.length,
                           m.rating_bayesian, u.name, COALESCE(rt.value, 0),
                           GROUP_CONCAT(u1.name, ', ')
                    FROM media m
                    INNER JOIN user u ON m.user_id = u.id
                    LEFT JOIN rating rt ON rt.user_id = ?
                        AND rt.media_id = m.id
                    INNER JOIN recommendation rc ON rc.media_id = m.id
                        AND rc.to_user_id = ?
                    LEFT JOIN user u1 ON u1.id = rc.from_user_id
                    GROUP BY m.title, m.author, m.description, m.length, u.name
                    ORDER BY SUM(rc.value) DESC
                    LIMIT ? """, (user_id, user_id, limit))
        else:
            cur = conn.cursor().execute(
                """ SELECT m.id, m.title, m.author, m.description, m.length,
                           m.rating_bayesian, u.name, COALESCE(rt.value, 0),
                           GROUP_CONCAT(u1.name, ', ')
                    FROM media m
                    INNER JOIN user u ON m.user_id = u.id
                    LEFT JOIN rating rt ON rt.user_id = ?
                        AND rt.media_id = m.id
                    INNER JOIN recommendation rc ON rc.media_id = m.id
                        AND rc.to_user_id = ?
                    LEFT JOIN user u1 ON u1.id = rc.from_user_id
                    LEFT JOIN status s ON s.user_id = ?
                        AND s.media_id = m.id
                    WHERE COALESCE(s.value, 0) NOT IN (2, 3)
                    GROUP BY m.title, m.author, m.description, m.length, u.name
                    ORDER BY SUM(rc.value) DESC
                    LIMIT ? """, (user_id, user_id, user_id, limit))

        return [dict(id=row[0], title=row[1], author=row[2],
                     description=row[3], length=row[4], rating=row[5],
                     username=row[6], personal_rating=row[7],
                     recommendations=row[8])
                for row in cur.fetchall()]
    except Exception as e:
        logger.error('get_recommended: caught exception')
        logger.exception(e)
        return list()


def get_recommendations_received(conn, user_id, media_id):
    try:
        cur = conn.cursor().execute(
            """ SELECT u.id, u.name, rc.value
                FROM recommendation rc
                INNER JOIN user u ON rc.from_user_id = u.id
                WHERE rc.media_id = ?
                    AND rc.to_user_id = ? """, (media_id, user_id))

        return [dict(id=media_id, user_id=row[0], username=row[1],
                     value=row[2])
                for row in cur.fetchall()]
    except Exception as e:
        logger.error('get_recommendations_received: caught exception')
        logger.exception(e)
        return list()


def get_recommendations_sent(conn, user_id, media_id):
    try:
        cur = conn.cursor().execute(
            """ SELECT u.id, u.name, rc.value
                FROM recommendation rc
                INNER JOIN user u ON rc.to_user_id = u.id
                WHERE rc.media_id = ?
                    AND rc.from_user_id = ? """, (media_id, user_id))

        return [dict(id=media_id, user_id=row[0], username=row[1],
                     value=row[2])
                for row in cur.fetchall()]
    except Exception as e:
        logger.error('get_recommendations_sent: caught exception')
        logger.exception(e)
        return list()


def get_status(conn, user_id, media_id):
    try:
        conn.cursor().execute(
            """ INSERT OR IGNORE INTO status (user_id, media_id, value)
                VALUES (?, ?, ?) """, (user_id, media_id, 0))
        conn.commit()

        cur = conn.cursor().execute(
            """ SELECT value
                FROM status
                WHERE user_id = ?
                    AND media_id = ? """, (user_id, media_id))

        return cur.fetchone()[0]
    except Exception as e:
        logger.error('get_status: caught exception')
        logger.exception(e)
        return 0


def get_top_rated(conn, user_id, include_read=False, limit=5):
    try:
        if include_read:
            cur = conn.cursor().execute(
                """ SELECT m.id, m.title, m.author, m.description, m.length,
                           m.rating_bayesian, u.name, COALESCE(rt.value, 0)
                    FROM media m
                    INNER JOIN user u ON m.user_id = u.id
                    LEFT JOIN rating rt ON rt.user_id = ?
                        AND rt.media_id = m.id
                    ORDER BY m.rating_bayesian DESC
                    LIMIT ? """, (user_id, limit))
        else:
            cur = conn.cursor().execute(
                """ SELECT m.id, m.title, m.author, m.description, m.length,
                           m.rating_bayesian, u.name, COALESCE(rt.value, 0)
                    FROM media m
                    INNER JOIN user u ON m.user_id = u.id
                    LEFT JOIN rating rt ON rt.user_id = ?
                        AND rt.media_id = m.id
                    LEFT JOIN status s ON s.user_id = ?
                        AND s.media_id = m.id
                    WHERE COALESCE(s.value, 0) NOT IN (2, 3)
                    ORDER BY m.rating_bayesian DESC
                    LIMIT ? """, (user_id, user_id, limit))

        return [dict(id=row[0], title=row[1], author=row[2],
                     description=row[3], length=row[4], rating=row[5],
                     username=row[6], personal_rating=row[7])
                for row in cur.fetchall()]
    except Exception as e:
        logger.error('get_top_rated: caught exception')
        logger.exception(e)
        return list()


def get_user_id_from_social(conn, social_id):
    try:
        cur = conn.cursor().execute(
            """ SELECT id
                FROM user
                WHERE id_social = ? """, (social_id, ))

        user = cur.fetchone()
        if user:
            return user[0]
        else:
            return None
    except Exception as e:
        logger.error('get_user_id_from_social: caught exception')
        logger.exception(e)
        return None


def get_users(conn):
    try:
        cur = conn.cursor().execute('SELECT id, name FROM user')

        return [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
    except Exception as e:
        logger.error('get_users: caught exception')
        logger.exception(e)
        return list()


def update_media(conn, media_id, updates):
    try:
        fields = ', '.join(['%s = ?' % k for k in updates.keys()])
        params = [v for v in updates.values() + [media_id]]

        conn.cursor().execute(
            """ UPDATE media
                SET %s
                WHERE id = ? """ % fields, params)
        conn.commit()

        return 200
    except Exception as e:
        logger.error('update_media: caught exception')
        logger.exception(e)
        return 500


def update_rating(conn, user_id, media_id, value):
    try:
        conn.cursor().execute(
            """ INSERT OR REPLACE INTO rating (user_id, media_id, value)
            VALUES (?, ?, ?) """, (user_id, media_id, value))
        conn.commit()

        return 200
    except Exception as e:
        logger.error('update_rating: caught exception')
        logger.exception(e)
        return 500


def update_recommendation(conn, from_user_id, to_user_id, media_id, value):
    try:
        conn.cursor().execute(
            """ INSERT OR REPLACE INTO recommendation (from_user_id,
                                                       to_user_id, media_id,
                                                       value)
                VALUES (?, ?, ?, ?) """, (from_user_id, to_user_id, media_id,
                                          value))
        conn.commit()

        return 200
    except Exception as e:
        logger.error('update_recommendation: caught exception')
        logger.exception(e)
        return 500


def update_status(conn, user_id, media_id, value):
    try:
        conn.cursor().execute(
            """ INSERT OR REPLACE INTO status (user_id, media_id, value)
                VALUES (?, ?, ?) """, (user_id, media_id, value))
        conn.commit()

        return 200
    except Exception as e:
        logger.error('update_status: caught exception')
        logger.exception(e)
        return 500
