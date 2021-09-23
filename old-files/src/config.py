import os


class Config(object):

    HARENA_LOGGER_FLASK_HOST         = os.environ.get('HARENA_LOGGER_FLASK_HOST',            '0.0.0.0')
    HARENA_LOGGER_FLASK_PORT         = int(os.environ.get('HARENA_LOGGER_FLASK_PORT',           10030))
    HARENA_LOGGER_FLASK_DEBUG        = bool(os.environ.get('HARENA_LOGGER_FLASK_DEBUG',         True))

    HARENA_LOGGER_MONGODB_HOST       = os.environ.get('HARENA_LOGGER_MONGODB_HOST',        'localhost')
    HARENA_LOGGER_MONGODB_PORT       = int(os.environ.get('HARENA_LOGGER_MONGODB_PORT',         10031))
    HARENA_LOGGER_MONGODB_URL        ="mongodb://{0}:{1}/".format(HARENA_LOGGER_MONGODB_HOST, HARENA_LOGGER_MONGODB_PORT)
    HARENA_LOGGER_MONGODB_DB         = os.environ.get('HARENA_LOGGER_MONGODB_DB',      'harena_logger')
    HARENA_LOGGER_MONGODB_COLLECTION = os.environ.get('HARENA_LOGGER_MONGODB_COLLECTION', 'event_logs')

    HARENA_LOGGER_KAFKA_BROKERS      = os.environ.get('HARENA_LOGGER_KAFKA_BROKERS', 'kafka1:19092')
    HARENA_LOGGER_KAFKA_TOPIC        = os.environ.get('HARENA_LOGGER_KAFKA_TOPIC', 'harena-logs')
    HARENA_LOGGER_INTERVAL_S         = int(os.environ.get('HARENA_LOGGER_INTERVAL_S', 10))


    # LOGGING SETTINGS
    LOGGING_NAME = os.environ.get('LOGGING_NAME', 'harena-logger')
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')

    LOGGING_STYLES = ('info=blue;'
                      'warning=green;'
                      'error=red;'
                      'critical=red,bold;'
                      'debug=white')

    LOGGING_FORMAT = ('%(asctime) -19s | %(levelname) -8s | %(threadName) -10s | '
                      '%(funcName) -16s | %(message)s')