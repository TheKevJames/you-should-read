import sanic


system = sanic.Blueprint('system')


@system.route('/ping')
async def ping(_request):
    """Simple healthcheck."""
    return sanic.response.text('pong')
