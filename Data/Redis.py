from config import REDIS_BROKER_HOST, REDIS_BROKER_PORT, REDIS_BROKER_USER, REDIS_BROKER_PASSWORD
import redis

redis = redis.Redis(
    host=REDIS_BROKER_HOST,
    port=int(REDIS_BROKER_PORT),
    username=REDIS_BROKER_USER,
    password=REDIS_BROKER_PASSWORD,
    decode_responses=True
) if REDIS_BROKER_USER != "" else redis.Redis(
    host=REDIS_BROKER_HOST,
    port=int(REDIS_BROKER_PORT),
    decode_responses=True
)