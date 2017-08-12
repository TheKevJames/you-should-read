#!/usr/bin/env python
import os

from server import app


HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', 80)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
