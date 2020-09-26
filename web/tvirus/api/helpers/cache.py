"""Redis SET/GET abstractions 
"""
import os
import redis
import hashlib

class RedisClient:
    """Base class for creating Redis based stuff.
    """
    DEFAULT_HOST = os.getenv('REDIS_HOST', 'localhost')
    DEFAULT_PORT = os.getenv('REDIS_PORT', 6379)
    DEFAULT_DB = int(os.getenv('REDIS_DB', 0))

    def __init__(self, *args, **kwargs):
        """Connect to redis using kwargs or env vars.

        Keyword Arguments
        -----------------
        host: str
            Redis Host
        port: int
            Redis Port
        db: int
            Redis DB
        """
        host = kwargs.get('host', self.DEFAULT_HOST)
        port = kwargs.get('port', self.DEFAULT_PORT)
        db = kwargs.get('db', self.DEFAULT_DB)
        self.r = redis.Redis(host=host,
          port=port,
          db=db
        )

    def get(self, key) -> bytes:
        return self.r.get(key)
    
    def set(self, key, val) -> bool:
        return self.r.set(key, val)

def cache_fingerprint(username: str, user_agent: str, uri: str) -> str:
    uname = f'USERNAME:sha256{hashlib.sha256(username.encode()).hexdigest()[:4]}'
    ua = f'USERAGENT:sha256{hashlib.sha256(user_agent.encode()).hexdigest()[:16]}'
    uri = f'URI:sha256{hashlib.sha256(uri.encode()).hexdigest()[:16]}'

    return f'{uname}{ua}{uri}'
