#!/usr/bin/env python

import os
import logging


class Config(object):
    # Basic app settings
    ENV = None
    DEBUG = True
    TESTING = False

    # JSON config
    JSON_INDENT = 4
    JSON_SORT_KEYS = True

    # Rate limit storage backend
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_STRATEGY = 'moving-window'
    RATELIMIT_HEADERS_ENABLED = False
    RATELIMIT_ENABLED = True

    # Security
    SECRET_KEY = 'REPLACE ME WITH SOMETHING ELSE!!!'
    USE_SSL = False

    # Logging
    LOG_FORMAT = '%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s'
    LOG_DATE_FORMAT = '%m/%d/%Y %H:%M:%S'
    DEFAULT_LOG_LEVEL = logging.DEBUG
    ERROR_404_HELP = False

    # Email configuration
    MAIL_USERNAME = os.getenv('MAILGUN_SMTP_LOGIN', 'test')
    MAIL_PASSWORD = os.getenv('MAILGUN_SMTP_PASSWORD', 'test')
    MAIL_SERVER = os.getenv('MAILGUN_SMTP_SERVER', 'test')
    MAIL_PORT = int(os.getenv('MAILGUN_SMPT_PORT', 587))
    MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS', True))
    MAIL_USE_SSL = bool(os.getenv('MAIL_USE_SSL', False))
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER',
                                    ('Trillium Pet Products '
                                     '<no-reply@trilliumpetproducts.com>'))
    MAIL_DEBUG = int(os.getenv('MAIL_DEBUG', 0))
    CONTACT_EMAIL_RECIPIENTS = os.getenv('CONTACT_EMAIL_RECIPIENTS')

    # Celery backend configuration
    REDIS_URL = 'redis://localhost'
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']

    # Celery task configuration
    CELERY_IMPORTS = ('trillium.tasks',)
    NOTIFICATION_FREQ_IN_SEC = 60
    CELERYBEAT_SCHEDULE = {}
    CELERYD_CONCURRENCY = 1
    BROKER_POOL_LIMIT = 8

    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    # CORS Settings
    CORS_ALLOW_HEADERS = (
        'Content-Type',
        'Authorization',
        'Origin',
    )
    CORS_ORIGINS = ('*',)
    CORS_ALWAYS_SEND = True

    PROFILE = bool(os.environ.get('PROFILE', False))

    # S3 Configuration
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', 'abc')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', '123')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET', 'example')
    AWS_URL_EXPIRY = int(os.getenv('AWS_URL_EXPIRY', 1000))


class TestConfig(Config):
    # Basic app settings
    ENV = 'test'
    TESTING = True

    # Security
    SECRET_KEY = 'test'

    # Ratelimit config
    RATELIMIT_ENABLED = False

    # Celery configuration
    CELERY_ALWAYS_EAGER = True

    # Database settings
    SQLALCHEMY_ECHO = False


class DevConfig(Config):
    """Development configuration."""
    # Basic app settings
    ENV = 'dev'

    # Rate limiter settings
    RATELIMIT_STORAGE_URL = 'redis://localhost'

    CORS_ORIGINS = (
        'http://localhost:5100',
    )


class ProdConfig(Config):
    """Staging configuration."""
    # Basic app settings
    ENV = 'production'
    DEBUG = False

    # CORS settings
    CORS_ORIGINS = (
        'http://trilliumpetproducts.com',
    )

    # Logging configuration
    DEFAULT_LOG_LEVEL = logging.INFO

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', Config.SECRET_KEY)

    # Celery backend configuration
    CELERY_BROKER_URL = os.getenv('REDIS_URL', Config.REDIS_URL)
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND',
                                           CELERY_BROKER_URL)
    BROKER_POOL_LIMIT = int(os.environ.get('BROKER_POOL_LIMIT',
                                           Config.BROKER_POOL_LIMIT))
    CELERYD_CONCURRENCY = int(os.environ.get('CELERYD_CONCURRENCY', 1))

    # Celery task settings
    NOTIFICATION_FREQ_IN_SEC = int(os.getenv('NOTIFICATION_FREQ_IN_SEC',
                                             Config.NOTIFICATION_FREQ_IN_SEC))

    # Rate limiter settings
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', Config.REDIS_URL)
    RATELIMIT_HEADERS_ENABLED = os.getenv('RATELIMIT_HEADERS_ENABLED', False)
