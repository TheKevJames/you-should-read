from __future__ import division

import logging

from you_should_read.db import get_media_ids
from you_should_read.db import get_media_rating_average
from you_should_read.db import get_media_rating_count
from you_should_read.db import get_ratings
from you_should_read.db import update_media


logger = logging.getLogger(__name__)


def update(conn, media_id):
    try:
        ratings = get_ratings(conn, media_id)
        rating_count = len(ratings)
        rating_average = sum(ratings) / rating_count

        code = update_media(conn, media_id, {'rating_average': rating_average})

        rating_counts = get_media_rating_count(conn)
        average_rating_count = sum(rating_counts) / len(rating_counts)

        average_rating_average = get_media_rating_average(conn)
        average_rating_total = average_rating_average * average_rating_count

        for media_id in get_media_ids(conn):
            ratings = get_ratings(conn, media_id)
            rating_count = len(ratings) or 1
            rating_average = sum(ratings) / rating_count
            rating_total = (rating_average * rating_count) or 1

            numerator = average_rating_total + rating_total
            denominator = rating_count + average_rating_count
            rating_bayes = numerator / denominator

            c = update_media(conn, media_id, {'rating_average': rating_average,
                                              'rating_bayesian': rating_bayes})
            code = code if code > c else c

        return code
    except Exception as e:
        logger.error('update: caught exception')
        logger.exception(e)
        return 500
