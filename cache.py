import time
import os

# sqlite-based cache
class cache_sqlite:

    connection = None
    cursor = None
    tables = []

    def __init__(self):

        # in-memory sqlite based cache
        self.connection = sqlite3.connect(':memory:', check_same_thread=False, isolation_level=None)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA journal_mode=wal")
        self.cursor.execute("PRAGMA wal_checkpoint=TRUNCATE")

        # start cache cleaning
        self.clean_cache()


    # cleans older than 60 seconds cache elements (those will be regenerated either way by update_hist_graph_scatter)
    def clean_cache(self):

        # run again in 30 seconds
        Timer(30, self.clean_cache).start()

        # clean old entries
        for table in self.tables:
            self.cursor.execute("DELETE FROM {} WHERE expires < ?".format(table), (int(time.time()),))

    # get cache element
    def get(self, pool, key):

        # table doesn't exist, so key can't as well
        if pool not in self.tables:
            return None

        # get data from cache
        result = self.cursor.execute("SELECT value FROM {} WHERE key = ?".format(pool), (key,)).fetchone()

        # no result
        if not result:
            return None

        # load pickle
        return pickle.loads(result[0])

    # set element in cache
    def set(self, pool, key, value, ttl=0):

        # if new pool, create table
        if pool not in self.tables:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {}(key TEXT PRIMARY KEY, value TEXT, expires INTEGER)".format(pool))
            self.cursor.execute("CREATE INDEX expires_{0} ON {0} (expires ASC)".format(pool))
            self.tables.append(pool)

        # store value with key
        self.cursor.execute("REPLACE INTO {} VALUES (?, ?, ?)".format(pool), (key, pickle.dumps(value), int(time.time() + ttl) if ttl > 0 and ttl <= 2592000 else ttl))

# memcached-based cache
class cache_memcached:

    client = None
    prefix = 'sentiment'

    def __init__(self):
        # in-memory memcached based cache
        self.client = memcache.Client(['localhost:11211'])

    # get cache element
    def get(self, pool, key):
        # get and return data from cache
        return self.client.get(self.prefix + '##' + pool + '##' + key.encode('ascii', 'xmlcharrefreplace').decode('ascii'))

    # set element in cache
    def set(self, pool, key, value, ttl=0):
        self.client.set(self.prefix + '##' + pool + '##' + key.encode('ascii', 'xmlcharrefreplace').decode('ascii'), value, ttl)


# import variable
cache = None

# if dev - use sqlite
if os.environ.get('dev', False):
    import sqlite3
    from threading import Timer
    import pickle

    cache = cache_sqlite()
# else - memcached
else:
    import memcache

    cache = cache_memcached()
