import raven


try:
    SENTRY_DSN = open('/run/secrets/sentry_dsn_ysr_server').read().rstrip()
except FileNotFoundError:
    SENTRY_DSN = None

sentry = raven.Client(SENTRY_DSN)
