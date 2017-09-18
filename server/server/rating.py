import asyncpg
import sanic

from .config import DATABASE_URL
from .view import BaseView


class RatingList(BaseView):
    async def get(self, _request):
        """Get all ratings.

        Returns:
            A list of JSON blobs containing each rating's data. Each item has
            the following format::

                {
                    'id': 42,
                    'uid': 12,
                    'mid': 3,
                    'value': 3.6,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }
        """
        return await super(RatingList, self).get_list('rating')

    async def post(self, request):
        """Create a rating.

        Args:
            request.json['uid'] (int): User ID for new rating.
            request.json['mid'] (int): Media ID for new rating.
            request.json['value'] (float): Value of new rating. Precision is to
                "xx.x".

        Returns:
            The id of the created rating::

                {'id': 42}

        Raises:
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: A
                required argument was not provided.
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: A value
                was too precise.
            :class:`InvalidUsage(409)<sanic:sanic.exceptions.InvalidUsage>`: A
                required resource did not exist.
        """
        uid = self.get_field(request, 'uid')
        mid = self.get_field(request, 'mid')
        value = self.get_field(request, 'value')

        try:
            return await super(RatingList, self).create_item(
                """ INSERT INTO ysr.rating (uid, mid, value)
                    VALUES ($1, $2, $3)
                    RETURNING id """, (uid, mid, value))
        except asyncpg.exceptions.NumericValueOutOfRangeError as e:
            raise sanic.exceptions.InvalidUsage(
                'value={} is too precise: {}'.format(value, str(e)))


class Rating(BaseView):
    async def delete(self, _request, rid):
        """Delete a single rating.

        Returns:
            null

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The rating does
                not exist.
        """
        return await super(Rating, self).delete_item('rating', rid)

    async def get(self, _request, rid):
        """Get a single rating.

        Returns:
            A JSON blob containing a single rating's data of the following
            format::

                {
                    'id': 42,
                    'uid': 12,
                    'mid': 3,
                    'value': 3.6,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The rating does
                not exist.
        """
        return await super(Rating, self).get_item('rating', rid)

    async def patch(self, request, rid):
        """Update a single rating.

        Args:
            request.json['value'] (float, optional): New value for rating.
                Precision is to "xx.x".

        Returns:
            A JSON blob containing the rating's new data of the following
            format::

                {
                    'id': 42,
                    'uid': 12,
                    'mid': 3,
                    'value': 3.7,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The rating does
                not exist.

        TODO:
            Raise exception when no patch body is provided.
        """
        current = await self.get(request, rid)

        value = self.get_field(request, 'value', default=current['value'])

        conn = await asyncpg.connect(dsn=DATABASE_URL)
        await conn.execute('UPDATE ysr.rating SET value=$1 WHERE id=$2', value,
                           rid)

        return await self.get(request, rid)


rating = sanic.Blueprint('rating', url_prefix='/rating')
rating.add_route(RatingList.as_view(), '/')
rating.add_route(Rating.as_view(), '/<rid:int>')
