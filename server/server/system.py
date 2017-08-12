from sanic.response import text

from . import app


@app.route('/ping')
async def ping(_request):
    """Simple healthcheck."""
    return text('pong')
