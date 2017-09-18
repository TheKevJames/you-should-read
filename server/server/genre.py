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
        conn = await asyncpg.connect(dsn=DATABASE_URL)
        rows = await conn.fetch('SELECT * FROM ysr.genre')
        return sanic.response.json(dict(r) for r in rows)

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

        conn = await asyncpg.connect(dsn=DATABASE_URL)
        gid = await conn.fetchval(
            """ INSERT INTO ysr.genre (name)
                VALUES ($1)
                RETURNING id """, name)
        return sanic.response.json({'id': gid}, status=201)


class Genre(BaseView):
    async def delete(self, request, gid):
        """Delete a single genre.

        Returns:
            null

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The genre does
                not exist.
        """
        await self.get(request, gid)

        conn = await asyncpg.connect(dsn=DATABASE_URL)
        await conn.execute('DELETE FROM ysr.genre WHERE id=$1', gid)
        return sanic.response.json(None, status=204)

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
        conn = await asyncpg.connect(dsn=DATABASE_URL)
        rows = await conn.fetch('SELECT * FROM ysr.genre WHERE id=$1', gid)

        try:
            return sanic.response.json(dict(rows[0]))
        except IndexError:
            raise sanic.exceptions.NotFound(
                'no genre with id {}'.format(gid))

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
