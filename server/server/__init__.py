import sanic

from server.bookmark import bookmark
from server.genre import genre
from server.media import media
from server.rating import rating
from server.recommendation import recommendation
from server.system import system
from server.user import user


app = sanic.Sanic('YouShouldRead')
app.blueprint(bookmark)
app.blueprint(genre)
app.blueprint(media)
app.blueprint(rating)
app.blueprint(recommendation)
app.blueprint(system)
app.blueprint(user)


@app.middleware('response')
async def set_response_headers(_request, response):
    response.headers['Access-Control-Allow-Headers'] = ', '.join(
        ('Content-Type', ))
    response.headers['Access-Control-Allow-Methods'] = ', '.join(
        ('GET', 'DELETE', 'PATCH', 'POST', 'PUT'))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'


__all__ = ['app']
