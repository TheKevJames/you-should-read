import asyncpg

import sanic

from . import DATABASE_URL, app


@app.route('/user')
async def get_users(_request):
    """Get all users.

    Returns the entire user table.

    Returns:
        A row of JSON blobs containing each user's data. Each item has the
        following format:

        {'id': 42, 'name': 'Billy Bob', 'created_at': _, 'updated_at': _}
    """
    conn = await asyncpg.connect(dsn=DATABASE_URL)
    rows = await conn.fetch('SELECT * FROM ysr.user')
    return sanic.response.json(dict(r) for r in rows)
