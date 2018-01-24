from time import time

import falcon
import redis


class RateLimiter(object):
    def __init__(self, limit=100, window=60):
        self.limit = limit
        self.window = window
        self.redis = redis.StrictRedis(host='redis', port=6379)

    def process_request(self, req, resp):
        requester = req.env['REMOTE_ADDR']

        key = "{0}: {1}".format(requester, req.path)
        print('Key: {0}'.format(key))

        try:
            remaining = self.limit - int(self.redis.get(key))
        except (ValueError, TypeError):
            remaining = self.limit
            self.redis.set(key, 0)

        expires_in = self.redis.ttl(key)

        if expires_in == -1:
            self.redis.expire(key, self.window)
            expires_in = self.window

        resp.append_header('X-RateLimit-Remaining: ', str(remaining - 1))
        resp.append_header('X-RateLimit-Limit: ', str(self.limit))
        resp.append_header('X-RateLimit-Reset: ', str(time() + expires_in))

        if remaining > 0:
            self.redis.incr(key, 1)
        else:
            raise falcon.HTTPTooManyRequests(
                title='Rate Limit Hit',
                description='Blocked: Too Many Requests'
            )
