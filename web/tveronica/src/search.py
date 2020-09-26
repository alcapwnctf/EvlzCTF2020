import os

import redis

PREFIX_DELIMITER = ':'

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

class KeyClient(RedisClient):
    """Implement prefix key manipulation.
    """
    def __init__(self, *args,  **kwargs):
        super(KeyClient, self).__init__(*args, )

    def get_total_keys(self, prefix):
        return len(
            self.r.keys(f'{prefix}{PREFIX_DELIMITER}*')
        )

    def search_prefix(self, prefix, query):
        return self.r.keys(f'{prefix}{PREFIX_DELIMITER}{query}*')
    
    def get_prefix(self, prefix, key):
        return self.r.get(f'{prefix}{PREFIX_DELIMITER}{key}')
    
    def write_prefix(self, prefix, key, value):
        return self.r.set(f'{prefix}{PREFIX_DELIMITER}{key}', value)
