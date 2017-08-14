import sanic


recommendation = sanic.Blueprint('recommendation',
                                 url_prefix='/recommendation')


class RecommendationList(sanic.views.HTTPMethodView):
    pass


class Recommendation(sanic.views.HTTPMethodView):
    pass


recommendation.add_route(RecommendationList.as_view(), '/')
recommendation.add_route(Recommendation.as_view(), '/<rid:int>')
