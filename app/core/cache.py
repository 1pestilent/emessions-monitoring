import pickle

from redis import Redis

from app.core.config import DB_HOST, REDIS_PORT,REDIS_PASSWORD

def connect_to_redis():
    return Redis(host=DB_HOST, port=REDIS_PORT)

def cache_data(key, data):
    cache = connect_to_redis()
    return cache.set(key, pickle.dumps(data))
    
def get_cached(key):
    cache = connect_to_redis()
    data = cache.get('last_query')
    if data:
        return pickle.loads(data)
    return None