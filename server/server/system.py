from sanic.exceptions import ServerError
from sanic.response import json, text

from . import app


@app.route('/ping')
async def ping(_request):
    """Simple healthcheck.
    """
    return text('pong')


@app.route('/doctest/<version:int>')
async def doctest(request, version):
    """Documentation test example.

    Checks to see if doc generation is working. Maybe I should use this as a
    template or something. Only succeeds according to arguments and some basic
    math, and only works for version 1.

    .. math:: 3 + 5 < 9^2

    Args:
        request.args['succeed']: Determine whether the operation will succeed.
            Valid values: 'yes', anything else.
        version: The version of the function to call. Only version 1 works.

    Returns:
        A json blob containing a success key and your input data.

        {'success': True, 'body': request.json}

    Raises:
        ServerError: An error occurred or inputs were incorrect.

    Todo:
        * Do stuff
    """
    if version != 1:
        raise ServerError('unsupported version {} != 1'.format(version), 500)

    if request.args.get('succeed') != 'yes':
        raise ServerError('did not send ?succeed=yes', 500)

    if 3 + 5 < 9 ** 2:
        return json({'success': True, 'body': request.json})
    else:
        raise ServerError('the universe is broken', 500)
