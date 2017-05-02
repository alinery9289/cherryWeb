import redis
from cherry.util.config import conf_dict
config = {
        'host': conf_dict['redis']['ip'], 
        'port': conf_dict['redis']['port'],
        'db': 0,
        }

r = redis.Redis(**config)
def redis_set(name, value):
    r.set(name, value)
def redis_get(name):
    return r.get(name)
def redis_has_key(name):
    return r.exists(name)
def redis_del(name):
    return r.delete(name)