import sanic

from .view import BaseView


class BookmarkList(BaseView):
    async def get(self, request):
        """Get all bookmarks.

        Returns:
            A list of JSON blobs containing each bookmark's data. Each item has
            the following format::

                {
                    'id': 42,
                    'uid': 12,
                    'mid': 3,
                    'url': 'https://example.com/page-3'
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }
        """
        return await super(BookmarkList, self).get_list(request.app.pool,
                                                        'bookmark')

    async def post(self, request):
        """Create a bookmark.

        Args:
            request.json['uid'] (int): User ID for new bookmark.
            request.json['mid'] (int): Media ID for new bookmark.
            request.json['url'] (str): URL of new bookmark.

        Returns:
            The id of the created bookmark::

                {'id': 42}

        Raises:
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: A
                required argument was not provided.
            :class:`InvalidUsage(409)<sanic:sanic.exceptions.InvalidUsage>`: A
                required resource did not exist.
        """
        uid = self.get_field(request, 'uid')
        mid = self.get_field(request, 'mid')
        url = self.get_field(request, 'url')

        return await super(BookmarkList, self).create_item(
            request.app.pool,
            """ INSERT INTO ysr.bookmark (uid, mid, url)
                VALUES ($1, $2, $3)
                RETURNING id """, (uid, mid, url))


class Bookmark(BaseView):
    async def delete(self, request, bid):
        """Delete a single bookmark.

        Returns:
            null

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The bookmark
                does not exist.
        """
        return await super(Bookmark, self).delete_item(request.app.pool,
                                                       'bookmark', bid)

    async def get(self, request, bid):
        """Get a single bookmark.

        Returns:
            A JSON blob containing a single bookmark's data of the following
            format::

                {
                    'id': 42,
                    'uid': 12,
                    'mid': 3,
                    'url': 'https://example.com/page-3'
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The bookmark
                does not exist.
        """
        return await super(Bookmark, self).get_item(request.app.pool,
                                                    'bookmark', bid)

    async def patch(self, request, bid):
        """Update a single bookmark.

        Args:
            request.json['url'] (str, optional): New URL for bookmark.

        Returns:
            A JSON blob containing the bookmark's new data of the following
            format::

                {
                    'id': 42,
                    'uid': 12,
                    'mid': 3,
                    'url': 'https://example.com/page-4'
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The bookmark
                does not exist.

        TODO:
            Raise exception when no patch body is provided.
        """
        current = await self.get(request, bid)

        url = self.get_field(request, 'url', default=current['url'])

        async with request.app.pool.acquire() as conn:
            await conn.execute('UPDATE ysr.bookmark SET url=$1 WHERE id=$2',
                               url, bid)

        return await self.get(request, bid)


bookmark = sanic.Blueprint('bookmark', url_prefix='/bookmark')
bookmark.add_route(BookmarkList.as_view(), '/')
bookmark.add_route(Bookmark.as_view(), '/<bid:int>')
