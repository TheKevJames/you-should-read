import sanic

from .config import sentry
from .bookmark import bookmark
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


@app.exception(sanic.exceptions.ServerError)
def send_exceptions_to_sentry(_request, _exception):
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
