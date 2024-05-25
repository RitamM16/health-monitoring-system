from os import getenv

# MySQL Config
MYSQL_HOST = getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_USER = getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = getenv("MYSQL_PASSWORD", "my-secret-pw")
MYSQL_PORT = getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = "monitoring"

# Celery CELERY_BROKER_URL Config
REDIS_BROKER_HOST = getenv("REDIS_HOST", "127.0.0.1")
REDIS_BROKER_PORT = getenv("REDIS_PORT", '6379')
REDIS_BROKER_USER = getenv("REDIS_USER", '')
REDIS_BROKER_PASSWORD = getenv("REDIS_PASSWORD", '')
# Celery CELERY_RESULT_BACKEND Config
REDIS_RESULT_HOST = getenv("REDIS_HOST", "127.0.0.1")
REDIS_RESULT_PORT = getenv("REDIS_PORT", '6379')
REDIS_RESULT_USER = getenv("REDIS_USER", '')
REDIS_RESULT_PASSWORD = getenv("REDIS_PASSWORD", '')

CELERY_BROKER_URL = f"redis://{REDIS_BROKER_HOST}:{REDIS_BROKER_PORT}@{REDIS_BROKER_USER}:{REDIS_BROKER_PASSWORD}/0" if REDIS_BROKER_USER != '' else f"redis://{REDIS_BROKER_HOST}:{REDIS_BROKER_PORT}/0"

CELERY_RESULT_BACKEND_URL = f"redis://{REDIS_RESULT_HOST}:{REDIS_RESULT_PORT}@{REDIS_RESULT_USER}:{REDIS_RESULT_PASSWORD}/0" if REDIS_RESULT_USER != '' else f"redis://{REDIS_RESULT_HOST}:{REDIS_RESULT_PORT}/0"

MYSQL_CONN_STRING = f'mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
MYSQL_CELERY_CONN_STRING = f'mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/scheduler'

SMTP_URL=getenv("SMTP_URL", 'localhost')