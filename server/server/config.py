import os

import raven


try:
    DATABASE_URL = open('/run/secrets/database_url').read().rstrip()
except FileNotFoundError:
    DATABASE_URL = os.environ.get('DATABASE_URL',
                                  'postgres://postgres@database:5432/postgres')

try:
    SENTRY_DSN = open('/run/secrets/secntry_dsn_ysr_server').read().rstrip()
except FileNotFoundError:
    SENTRY_DSN = None

sentry = raven.Client(SENTRY_DSN)
