import asyncpg
import sanic

from server.config import DATABASE_URL


class BaseView(sanic.views.HTTPMethodView):
    @staticmethod
    async def create_item(query, queryargs):
        """Do a database insert.

        Args:
            query (str): Query string to execute.
            queryargs (list of str): Arguments to query string.

        Returns:
            The id of the created item::

                {'id': 42}

        Raises:
            :class:`asyncpg.exceptions.CheckViolationError`: The database
                failed a CHECK on the new item.
            :class:`asyncpg.exceptions.NumericValueOutOfRangeError`: The
                database could not accept an overly precise value.
            :class:`InvalidUsage(409)<sanic:sanic.exceptions.InvalidUsage>`:
                New item had invalid foreign keys.
        """
        conn = await asyncpg.connect(dsn=DATABASE_URL)
        try:
            uuid = await conn.fetchval(query, *queryargs)
        except asyncpg.exceptions.ForeignKeyViolationError as e:
            raise sanic.exceptions.InvalidUsage(
                'item had invalid foreign keys: {}'.format(str(e)),
                status_code=409)

        return sanic.response.json({'id': uuid}, status=201)

    @staticmethod
    async def delete_item(table, uuid):
        """Delete a single item from a table by ID.

        Args:
            table (str): Name of table to search.
            uuid (int): ID of item to delete.

        Returns:
            null

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: Data with the
                specified ID does not exist on this table.
        """
        await BaseView.get_item(table, uuid)

        conn = await asyncpg.connect(dsn=DATABASE_URL)
        query = 'DELETE FROM ysr.{} WHERE id=$1'.format(table)
        await conn.execute(query, uuid)
        return sanic.response.json(None, status=204)

    @staticmethod
    def get_field(request, field, default=None):
        """Helper method for getting a specified field from the JSON fields in
        a request object.

        Args:
            request: A :class:`Request<sanic:sanic.request.Request>`
            field (str): Field to be looked up.
            default (optional): Default value to return if the field is
                missing.

        Returns:
            The value of the specified field contained in the request object,
            if present. If the field is missing but a default was provided,
            returns the default object.

        Raises:
            :class:`InvalidUsage<sanic:sanic.exceptions.InvalidUsage>`: The
                field was not provided and no default was set.
        """
        try:
            return request.json[field]
        except KeyError:
            if default is not None:
                return default

            raise sanic.exceptions.InvalidUsage(
                'missing {} field'.format(field))

    @staticmethod
    async def get_item(table, uuid):
        """Get a single item from a table by ID.

        Args:
            table (str): Name of table to search.
            uuid (int): ID of item to get.

        Returns:
            A JSON blob containing the data of an object. Always contains the
            following::

                {
                    'id': 42,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }

        Raises:
            :class:`NotFound<sanic:sanic.exceptions.NotFound>`: Data with the
                specified ID does not exist on this table.
        """
        conn = await asyncpg.connect(dsn=DATABASE_URL)
        query = 'SELECT * FROM ysr.{} WHERE id=$1'.format(table)
        rows = await conn.fetch(query, uuid)

        try:
            return sanic.response.json(dict(rows[0]))
        except IndexError:
            raise sanic.exceptions.NotFound('no {} with id {}'.format(table,
                                                                      uuid))

    @staticmethod
    async def get_list(table):
        """Get all items from a table.

        Args:
            table (str): Name of table to search.

        Returns:
            A list of JSON blobs containing the data of an object. Each item
            always contains the following::

                {
                    'id': 42,
                    'created_at': 1502680672,
                    'updated_at': 1502680672
                }
        """
        conn = await asyncpg.connect(dsn=DATABASE_URL)
        rows = await conn.fetch('SELECT * FROM ysr.{}'.format(table))
        return sanic.response.json(dict(r) for r in rows)
