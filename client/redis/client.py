import os, os.path
import time

import redis

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')

r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)
limit=1000
for i in limit:
    r.set('foo' + i, 'bar')
    time.sleep(5)
    print ("waiting for 5 sec..")
