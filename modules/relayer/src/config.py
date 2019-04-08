import os

class Config(object):

    HARENA_LOGGER_BROKER_HOST        = os.environ.get('HARENA_LOGGER_BROKER_HOST',         'localhost')
    HARENA_LOGGER_BROKER_PORT        = int(os.environ.get('HARENA_LOGGER_BROKER_PORT',           1883))

    HARENA_LOGGER_FLASK_HOST         = os.environ.get('HARENA_LOGGER_FLASK_HOST',            '0.0.0.0')
    HARENA_LOGGER_FLASK_PORT         = int(os.environ.get('HARENA_LOGGER_FLASK_PORT',            5000))
    HARENA_LOGGER_FLASK_DEBUG        = bool(os.environ.get('HARENA_LOGGER_FLASK_DEBUG',         False))

    HARENA_LOGGER_MONGODB_HOST       = os.environ.get('HARENA_LOGGER_MONGODB_HOST',        'localhost')
    HARENA_LOGGER_MONGODB_PORT       = int(os.environ.get('HARENA_LOGGER_MONGODB_PORT',         27017))
    HARENA_LOGGER_MONGODB_DB         = os.environ.get('HARENA_LOGGER_MONGODB_DB',      'harena_logger')
    HARENA_LOGGER_MONGODB_COLLECTION = os.environ.get('HARENA_LOGGER_MONGODB_COLLECTION', 'executions')
