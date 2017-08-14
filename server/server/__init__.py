import os

import sanic


DATABASE_URL = os.environ.get('DATABASE_URL',
                              'postgres://postgres@database:5432/postgres')

app = sanic.Sanic('YouShouldRead')


from server import system  # pylint: disable=C0413
from server import user  # pylint: disable=C0413


__all__ = ['DATABASE_URL', 'app', 'system', 'user']
