#it for local memory redis

import time

requests_log = {}

def is_allowed(ip):
    limit = 10
    window = 10

    now = time.time()

    if ip not in requests_log:
        requests_log[ip] = []

    requests_log[ip] = [
        t for t in requests_log[ip] if now - t < window
    ]

    if len(requests_log[ip]) >= limit:
        return False

    requests_log[ip].append(now)
    return True



# redis 
#import redis

#r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

#def is_allowed(ip):
    key = f"rate:{ip}"
    limit = 10
    window = 10

    #try:
        #current = r.get(key)

        #if current and int(current) >= limit:
            #return False

        #pipe = r.pipeline()
        #pipe.incr(key, 1)
        #pipe.expire(key, window)
        #pipe.execute()

        #return True

    #except Exception as e:
        #print("Redis error:", e)
        #return True  # fallback: allow request