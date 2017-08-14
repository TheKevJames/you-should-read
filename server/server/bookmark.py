import sanic


bookmark = sanic.Blueprint('bookmark', url_prefix='/bookmark')


class BookmarkList(sanic.views.HTTPMethodView):
    pass


class Bookmark(sanic.views.HTTPMethodView):
    pass


bookmark.add_route(BookmarkList.as_view(), '/')
bookmark.add_route(Bookmark.as_view(), '/<bid:int>')
