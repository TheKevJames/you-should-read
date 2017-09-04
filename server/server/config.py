import os


try:
    DATABASE_URL = open('/run/secrets/database_url').read().rstrip()
except FileNotFoundError:
    DATABASE_URL = os.environ.get('DATABASE_URL',
                                  'postgres://postgres@database:5432/postgres')
