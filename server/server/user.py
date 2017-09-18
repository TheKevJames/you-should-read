import asyncpg
import sanic

from .config import DATABASE_URL
from .view import BaseView


class UserList(BaseView):
    async def get(self, _request):
        """Get all users.

        Returns:
            A list of JSON blobs containing each user's data. Each item has the
            following format::

                {
                    'id': 42,
                    'name': 'Billy Bob',
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }
        """
        return await super(UserList, self).get_list('user')

    async def post(self, request):
        """Create a user.

        Args:
            request.json['name'] (str): Name of new user.

        Returns:
            The id of the created user::

                {'id': 42}

        Raises:
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: A
                required argument was not provided.
        """
        name = self.get_field(request, 'name')

        return await super(UserList, self).create_item(
            """ INSERT INTO ysr.user (name)
                VALUES ($1)
                RETURNING id """, (name, ))


class User(BaseView):
    async def delete(self, _request, uid):
        """Delete a single user.

        Returns:
            null

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The user does
                not exist.
        """
        return await super(User, self).delete_item('user', uid)

    async def get(self, _request, uid):
        """Get a single user.

        Returns:
            A JSON blob containing a single user's data of the following
            format::

                {
                    'id': 42,
                    'name': 'Billy Bob',
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The user does
                not exist.
        """
        return await super(User, self).get_item('user', uid)

    async def patch(self, request, uid):
        """Update a single user.

        Args:
            request.json['name'] (str, optional): New name for user.

        Returns:
            A JSON blob containing the user's new data of the following
            format::

                {
                    'id': 42,
                    'name': 'Billie Bob',
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: The user does
                not exist.

        TODO:
            Raise exception when no patch body is provided.
        """
        current = await self.get(request, uid)

        name = self.get_field(request, 'name', default=current['name'])

        conn = await asyncpg.connect(dsn=DATABASE_URL)
        await conn.execute('UPDATE ysr.user SET name=$1 WHERE id=$2', name,
                           uid)

        return await self.get(request, uid)


user = sanic.Blueprint('user', url_prefix='/user')
user.add_route(UserList.as_view(), '/')
user.add_route(User.as_view(), '/<uid:int>')
# TODO:
# /user/<uid>/rating
# /user/<uid>/rating/<rtid>
# /user/<uid>/bookmark
# /user/<uid>/bookmark/<bmid>
# /user/<uid>/recommendation-send
# /user/<uid>/recommendation-send/<rid>
# /user/<uid>/recommendation-receive
# /user/<uid>/recommendation-receive/<rid>
