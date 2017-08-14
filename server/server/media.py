import sanic


media = sanic.Blueprint('media', url_prefix='/media')
media_genre = sanic.Blueprint('media_genre',
                              url_prefix='/media/<mid:int>/genre')


class MediaList(sanic.views.HTTPMethodView):
    pass


class Media(sanic.views.HTTPMethodView):
    pass


class MediaGenreList(sanic.views.HTTPMethodView):
    pass


class MediaGenre(sanic.views.HTTPMethodView):
    pass


media.add_route(MediaList.as_view(), '/')
media.add_route(Media.as_view(), '/<mid:int>')
media_genre.add_route(MediaGenreList.as_view(), '/')
media_genre.add_route(MediaGenre.as_view(), '/<gid:int>')
