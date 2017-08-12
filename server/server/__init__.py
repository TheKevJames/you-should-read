from sanic import Sanic


app = Sanic('YouShouldRead')


from server import system  # pylint: disable=C0413


__all__ = ['app', 'system']
