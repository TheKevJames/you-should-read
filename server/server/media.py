import asyncpg
import sanic

from .view import BaseView


class MediaList(BaseView):
    async def get(self, request):
        """Get all media.

        Returns:
            A list of JSON blobs containing each media's data. Each item has
            the following format::

                {
                    'id': 42,
                    'name': "Hitchhiker's Guide to the Galaxy",
                    'url': 'https://hitchhikersguide.com/',
                    'rating': 9.3297,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }
        """
        return await super(MediaList, self).get_list(request.app.pool, 'media')

    async def post(self, request):
        """Create a media.

        Args:
            request.json['name'] (str): Name of the new media.
            request.json['url'] (str, optional): URL of the new media.

        Returns:
            The id of the created media::

                {'id': 42}

        Raises:
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: A
                required argument was not provided.
        """
        name = self.get_field(request, 'name')
        url = request.json.get('url')

        return await super(MediaList, self).create_item(
            request.app.pool,
            """ INSERT INTO ysr.media (name, url)
                VALUES ($1, $2)
                RETURNING id """, (name, url))


class Media(BaseView):
    async def delete(self, request, mid):
        """Delete a single media.

        Returns:
            null

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The media does
                not exist.
        """
        return await super(Media, self).delete_item(request.app.pool, 'media',
                                                    mid)

    async def get(self, request, mid):
        """Get a single media.

        Returns:
            A JSON blob containing a single media's data of the following
            format::

                {
                    'id': 42,
                    'name': "Hitchhiker's Guide to the Galaxy",
                    'url': 'https://hitchhikersguide.com/',
                    'rating': 9.3297,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The media does
                not exist.
        """
        return await super(Media, self).get_item(request.app.pool, 'media',
                                                 mid)

    async def patch(self, request, mid):
        """Update a single media.

        Args:
            request.json['name'] (str, optional): New name for media.
            request.json['url'] (str, optional): New url for media.

        Returns:
            A JSON blob containing the media's new data of the following
            format::

                {
                    'id': 42,
                    'name': "Hitchhiker's Guide to the Galaxy",
                    'url': 'https://hitchhikersguideofthegalaxy.com/',
                    'rating': 9.3297,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The media does
                not exist.

        TODO:
            Raise exception when no patch body is provided.
        """
        current = await self.get(request, mid)

        name = self.get_field(request, 'name', default=current['name'])
        url = self.get_field(request, 'url', default=current['url'])

        async with request.app.pool.acquire() as conn:
            await conn.execute(
                """ UPDATE ysr.media
                    SET name=$1, url=$2 WHERE id=$2 """, name,
                url, mid)

        return await self.get(request, mid)


class MediaGenreList(BaseView):
    async def get(self, request, mid):
        """Get all genres for this media.

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
        async with request.app.pool.acquire() as conn:
            rows = await conn.fetch(
                """ SELECT g.id, g.name, g.created_at, g.updated_at
                    FROM ysr.genre g
                    INNER JOIN ysr.media_genre mg ON mg.gid = g.id
                    WHERE mg.mid=$1 """, mid)

        return sanic.response.json(dict(r) for r in rows)

    async def post(self, request, mid):
        """Add a new genre to this media.

        Args:
            request.json['gid'] (int): Genre ID for new media_genre.

        Returns:
            The id of the created media_genre::

                {'id': 42}

        Raises:
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: A
                required argument was not provided.
            :class:`InvalidUsage(409)<sanic:sanic.exceptions.InvalidUsage>`: A
                required resource did not exist.
        """
        gid = self.get_field(request, 'gid')

        async with request.app.pool.acquire() as conn:
            try:
                mgid = await conn.fetchval(
                    """ INSERT INTO ysr.media_genre (mid, gid)
                        VALUES ($1, $2)
                        RETURNING id """, mid, gid)
            except asyncpg.exceptions.ForeignKeyViolationError as e:
                raise sanic.exceptions.InvalidUsage(
                    'media_genre had invalid foreign keys: {}'.format(str(e)),
                    status_code=409)

        return sanic.response.json({'id': mgid}, status=201)


class MediaGenre(BaseView):
    async def delete(self, request, mid, gid):
        """Remove a genre from this media.

        Returns:
            null

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The genre did
                not exist on this media.
        """
        await self.get(request, mid, gid)

        async with request.app.pool.acquire() as conn:
            await conn.execute(
                """ DELETE FROM ysr.media_genre
                    WHERE mid=$1 AND gid=$2 """, mid, gid)

        return sanic.response.json(None, status=204)

    async def get(self, request, mid, gid):
        """Get a single genre on this media.

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
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The media_genre
                does not exist.
        """
        async with request.app.pool.acquire() as conn:
            rows = await conn.fetch(
                """ SELECT g.id, g.name, g.created_at, g.updated_at
                    FROM ysr.genre g
                    INNER JOIN ysr.media_genre mg ON mg.gid = g.id
                    WHERE mg.mid=$1 AND mg.gid=$2 """, mid, gid)

        try:
            return sanic.response.json(dict(rows[0]))
        except IndexError:
            raise sanic.exceptions.NotFound(
                'no genre with id {} on media {}'.format(gid, mid))


media = sanic.Blueprint('media', url_prefix='/media')
media.add_route(MediaList.as_view(), '/')
media.add_route(Media.as_view(), '/<mid:int>')
media.add_route(MediaGenreList.as_view(), '/<mid:int>/genre')
media.add_route(MediaGenre.as_view(), '/<mid:int>/genre/<gid:int>')
