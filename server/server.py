#!/usr/bin/env python
import os

from sanic import Sanic
from sanic.response import json


PORT = os.environ.get('PORT', 80)


app = Sanic()


@app.route('/')
async def test(_request):
    return json({'hello': 'world'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
