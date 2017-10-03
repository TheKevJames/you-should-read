import sanic


system = sanic.Blueprint('system')


@system.route('/ping', methods=['GET', 'HEAD'])
async def ping(_request):
    """Simple healthcheck."""
    return sanic.response.text('pong')
