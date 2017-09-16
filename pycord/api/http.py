import asyncio
import aiohttp


class Route:

    BASE = 'https://discordapp.com/api/v7'

    def __init__(self, method, path, **params):
        self.method = method
        self.path = path.format(**params)
        self.channel = params.get('channel')
        self.guild = params.get('guild')
        self.url = self.BASE + self.path

    @property
    def bucket(self):
        return f'{self.method}.{self.path}.{self.channel}.{self.guild}'

class RateLimiter:
    def __init__(self, lock):
        self.lock = lock

    async def __aenter__(self):
        await self.lock
        return self

    async def __aexit__(self, type, value, traceback):
        if self.unlock:
            self.lock.release()  

    def delay(self):
        self.unlock = False



class HttpClient:
    def __init__(self, loop=None, connector=None):
        self.loop = loop or asyncio.get_event_loop()
        self.connector = connector
        self.session = aiohttp.ClientSession(loop=self.loop, connector=connector)
        self.token = None
        self.is_bot = True
        self.bucket_locks = weakref.WeakValueDictionary()
        self.global_lock = asyncio.Lock(loop=self.loop)
        self.global_lock.set()

    async def request(self, method, route, **kwargs):
        method = route.method
        bucket = route.bucket
        url = route.url

        lock = self.bucket_locks.get(bucket)
        if not lock:
            lock = asyncio.Lock(loop=self.loop)
            if bucket:
                self.bucket_locks[bucket] = lock

        token = 'Bot '+self.token if self.is_bot else self.token
        headers = {'Authorization': token}

        async with RateLimiter(lock) as throttle:
            async with self.session.request(method, url, headers=headers, **kwargs) as resp:
                data = await resp.json()
                remaining = resp.headers.get('X-Ratelimit-Remaining')

                if remaining == '0': #simple ratelimiting
                    delta = self._parse_ratelimit_header(resp)
                    throttle.delay()
                    self.loop.call_later(delta, self.lock.release)

                if resp.status >= 400:
                    raise RuntimeError(f"HTTP Error {resp.status}: {resp.reason}")

                if 200 <= resp.status < 300:
                    return data








