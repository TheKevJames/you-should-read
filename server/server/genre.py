import asyncpg
import sanic

from .config import DATABASE_URL
from .view import BaseView


class GenreList(BaseView):
    async def get(self, _request):
        """Get all genres.

        Returns:
            A list of JSON blobs containing each genre's data. Each item has
            the following format::

                {
                    'id': 42,
                    'name': 'fantasy'
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }
        """
        return await super(GenreList, self).get_list('genre')

    async def post(self, request):
        """Create a genre.

        Args:
            request.json['name'] (str): Name of new genre.

        Returns:
            The id of the created genre::

                {'id': 42}

        Raises:
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: A
                required argument was not provided.
        """
        name = self.get_field(request, 'name')

        return await super(GenreList, self).create_item(
            """ INSERT INTO ysr.genre (name)
                VALUES ($1)
                RETURNING id """, (name, ))


class Genre(BaseView):
    async def delete(self, _request, gid):
        """Delete a single genre.

        Returns:
            null

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The genre does
                not exist.
        """
        return await super(Genre, self).delete_item('genre', gid)

    async def get(self, _request, gid):
        """Get a single genre.

        Returns:
            A JSON blob containing a single genre's data of the following
            format::

                {
                    'id': 42,
                    'name': 'fantasy'
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The genre does
                not exist.
        """
        return await super(Genre, self).get_item('genre', gid)

    async def patch(self, request, gid):
        """Update a single genre.

        Args:
            request.json['name'] (str, optional): New name for genre.

        Returns:
            A JSON blob containing the genre's new data of the following
            format::

                {
                    'id': 42,
                    'name': 'not-fantasy'
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The genre does
                not exist.

        TODO:
            Raise exception when no patch body is provided.
        """
        current = await self.get(request, gid)

        name = self.get_field(request, 'name', default=current['name'])

        conn = await asyncpg.connect(dsn=DATABASE_URL)
        await conn.execute('UPDATE ysr.genre SET name=$1 WHERE id=$2', name,
                           gid)

        return await self.get(request, gid)


genre = sanic.Blueprint('genre', url_prefix='/genre')
genre.add_route(GenreList.as_view(), '/')
genre.add_route(Genre.as_view(), '/<gid:int>')
