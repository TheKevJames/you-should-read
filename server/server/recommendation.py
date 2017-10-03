import asyncpg
import sanic

from .view import BaseView


class RecommendationList(BaseView):
    async def get(self, request):
        """Get all recommendations.

        Returns:
            A list of JSON blobs containing each recommendation's data. Each
            item has the following format::

                {
                    'id': 42,
                    'fuid': 12,
                    'tuid': 14,
                    'mid': 3,
                    'value': 3.6,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }
        """
        return await super(RecommendationList, self).get_list(request.app.pool,
                                                              'recommendation')

    async def post(self, request):
        """Create a recommendation.

        Args:
            request.json['fuid'] (int): User ID making new recommendation.
            request.json['tuid'] (int): User ID being given new recommendation.
            request.json['mid'] (int): Media ID for new recommendation.
            request.json['value'] (float): Value of new recommendation.
                Precision is to "xx.x".

        Returns:
            The id of the created recommendation::

                {'id': 42}

        Raises:
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: A
                required argument was not provided.
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: A value
                was too precise.
            :class:`InvalidUsage(409)<sanic:sanic.exceptions.InvalidUsage>`: A
                required resource did not exist.
            :class:`InvalidUsage(422)<sanic:sanic.exceptions.InvalidUsage>`:
                Attempted to recommend to self.
        """
        fuid = self.get_field(request, 'fuid')
        tuid = self.get_field(request, 'tuid')
        mid = self.get_field(request, 'mid')
        value = self.get_field(request, 'value')

        try:
            return await super(RecommendationList, self).create_item(
                request.app.pool,
                """ INSERT INTO ysr.recommendation (fuid, tuid, mid, value)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id """, (fuid, tuid, mid, value))
        except asyncpg.exceptions.CheckViolationError:
            raise sanic.exceptions.InvalidUsage('cannot recommend to self',
                                                status_code=422)
        except asyncpg.exceptions.NumericValueOutOfRangeError as e:
            raise sanic.exceptions.InvalidUsage(
                'value={} is too precise: {}'.format(value, str(e)))


class Recommendation(BaseView):
    async def delete(self, request, rid):
        """Delete a single recommendation.

        Returns:
            null

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The
                recommendation does not exist.
        """
        return await super(Recommendation, self).delete_item(request.app.pool,
                                                             'recommendation',
                                                             rid)

    async def get(self, request, rid):
        """Get a single recommendation.

        Returns:
            A JSON blob containing a single recommendation's data of the
            following format::

                {
                    'id': 42,
                    'fuid': 12,
                    'tuid': 14,
                    'mid': 3,
                    'value': 3.6,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The
                recommendation does not exist.
        """
        return await super(Recommendation, self).get_item(request.app.pool,
                                                          'recommendation',
                                                          rid)

    async def patch(self, request, rid):
        """Update a single recommendation.

        Args:
            request.json['value'] (float, optional): New value for
                recommendation. Precision is to "xx.x".

        Returns:
            A JSON blob containing the recommendation's new data of the
            following format::

                {
                    'id': 42,
                    'fuid': 12,
                    'tuid': 14,
                    'mid': 3,
                    'value': 3.7,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The
                recommendation does not exist.

        TODO:
            Raise exception when no patch body is provided.
        """
        current = await self.get(request, rid)

        value = self.get_field(request, 'value', default=current['value'])

        async with request.app.pool.acquire() as conn:
            await conn.execute(
                """ UPDATE ysr.recommendation
                    SET value=$1 WHERE id=$2 """, value, rid)

        return await self.get(request, rid)


recommendation = sanic.Blueprint('recommendation',
                                 url_prefix='/recommendation')
recommendation.add_route(RecommendationList.as_view(), '/')
recommendation.add_route(Recommendation.as_view(), '/<rid:int>')
