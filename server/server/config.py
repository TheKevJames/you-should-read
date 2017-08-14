import os


DATABASE_URL = os.environ.get('DATABASE_URL',
                              'postgres://postgres@database:5432/postgres')
