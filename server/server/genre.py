import sanic


genre = sanic.Blueprint('genre', url_prefix='/genre')


class GenreList(sanic.views.HTTPMethodView):
    pass


class Genre(sanic.views.HTTPMethodView):
    pass


genre.add_route(GenreList.as_view(), '/')
genre.add_route(Genre.as_view(), '/<gid:int>')
