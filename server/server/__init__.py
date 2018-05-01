import os

import asyncpg
import sanic

from .bookmark import bookmark
from .config import sentry
from .genre import genre
from .media import media
from .rating import rating
from .recommendation import recommendation
from .system import system
from .user import user


app = sanic.Sanic('YouShouldRead')
app.blueprint(bookmark)
app.blueprint(genre)
app.blueprint(media)
app.blueprint(rating)
app.blueprint(recommendation)
app.blueprint(system)
app.blueprint(user)


@app.listener('after_server_start')
async def attach_pgpool(app, loop):  # pylint: disable=redefined-outer-name
    try:
        DATABASE_URL = open('/run/secrets/database_url').read().rstrip()

        # require ssl in production
        import ssl
        ssl_context = ssl.SSLContext()
        app.pool = await asyncpg.create_pool(dsn=DATABASE_URL, ssl=ssl_context,
                                             min_size=5, max_size=5, loop=loop)
    except FileNotFoundError:
        DATABASE_URL = os.environ.get(
            'DATABASE_URL', 'postgres://postgres@database:5432/postgres')
        app.pool = await asyncpg.create_pool(dsn=DATABASE_URL, loop=loop)


@app.exception(Exception)
def send_exceptions_to_sentry(request, exception):  # pylint: disable=unused-argument
    sentry.captureException()


@app.middleware('response')
async def set_response_headers(_request, response):
    response.headers['Access-Control-Allow-Headers'] = ', '.join(
        ('Content-Type', ))
    response.headers['Access-Control-Allow-Methods'] = ', '.join(
        ('GET', 'DELETE', 'PATCH', 'POST', 'PUT'))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'


__all__ = ['app']
