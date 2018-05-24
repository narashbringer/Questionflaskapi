import os
postgres_local_base = 'postgresql://postgres:123456@localhost/'
database_name = 'api'
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/questionrest_test'
    DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv( 'DATABASE_URL', postgres_local_base + database_name)
   
class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv( 'DATABASE_URL', postgres_local_base + database_name)
    BCRYPT_HASH_PREFIX = 13

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}