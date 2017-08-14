import sanic


rating = sanic.Blueprint('rating', url_prefix='/rating')


class RatingList(sanic.views.HTTPMethodView):
    pass


class Rating(sanic.views.HTTPMethodView):
    pass


rating.add_route(RatingList.as_view(), '/')
rating.add_route(Rating.as_view(), '/<rid:int>')
