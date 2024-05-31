import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or ''
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True