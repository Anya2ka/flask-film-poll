import os


DATABASE = {
    'HOST': os.getenv('DATABASE_HOST', 'localhost'),
    'PORT': int(os.getenv('DATABASE_PORT', '27017')),
    'NAME': os.getenv('DATABASE_NAME', 'film-find'),
}
