import sys
import gzip
import time
import asyncio
import aiohttp
<<<<<<< HEAD
import weakref
from urllib.parse import quote
from .. import __version__, __github__
from ..utils import get_event_loop, to_json, from_json, API
=======
from .. import utils


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
        await self.lock`
        return self

    async def __aexit__(self, type, value, traceback):
        if self.unlock:
            self.lock.release()  

    def delay(self):
        self.unlock = False
>>>>>>> e6938cd81dad3fa86c3c4033a988ea6fc18a6f6c

class HoldableLock:
    __slots__ = ('lock', 'unlock')
    def __init__(self, lock):
        self.unlock, self.lock = True, lock

    def hold(self):
        self.unlock = False

    async def __aenter__(self):
        await self.lock.acquire()
        return self

    async def __aexit__(self, *args):
        if self.unlock:
            self.lock.release()

class GlobalLock:
    __slots__ = ('global_event', 'is_global')
    def __init__(self, global_event, is_global):
        self.is_global = is_global
        self.global_event = global_event
    
    def __enter__(self):
        if self.is_global:
            self.global_event.clear()

    def __exit__(self, *args):
        if self.is_global:
            self.global_event.set()

class HttpClient:
    def __init__(self, loop=None):
        self.token = None
<<<<<<< HEAD
        self.retries = 5
        self.loop = loop or get_event_loop()
        self.buckets = weakref.WeakValueDictionary()
        self.global_event = asyncio.Event(loop=self.loop)
        self.session = aiohttp.ClientSession(loop=self.loop)

        # set global lock and create user agent
        self.global_event.set()
        user_agent = 'DiscordBot ({0} {1}) Python/{2[0]}.{2[1]}'
        self.user_agent = user_agent.format(
            __github__, __version__, sys.version_info)

    def __del__(self):
        self.session.close()

    async def get(self, endpoint, **kwargs):
        ''' Helper function for GET request '''
        return await self.request('GET', endpoint, **kwargs)

    async def put(self, endpoint, **kwargs):
        ''' Helper function for PUT request '''
        return await self.request('PUT', endpoint, **kwargs)

    async def post(self, endpoint, **kwargs):
        ''' Helper function for POST request '''
        return await self.request('POST', endpoint, **kwargs)

    async def patch(self, endpoint, **kwargs):
        ''' Helper function for PATCH request '''
        return await self.request('PATCH', endpoint, **kwargs)

    async def delete(self, endpoint, **kwargs):
        ''' Helper function for DELETE request '''
        return await self.request('DELETE', endpoint, **kwargs)

    async def request(self, method, endpoint, **kwargs):
        ''' Perform an HTTP request with rate limiting '''
        method = method
        endpoint = endpoint
        bucket = f"{method}.{endpoint}"
        endpoint = API.HTTP_ENDPOINT + endpoint

        # get route
        lock = self.buckets.get(bucket)
        if lock is None:
            lock = asyncio.Lock(loop=self.loop)
            self.buckets[bucket] = lock

        # create headers
        headers = {'User-Agent': self.user_agent}
        if self.token is not None:
            headers['Authorization'] = f'Bot {self.token}'
        if 'reason' in kwargs:
            headers['X-Audit-Log-Reason'] = kwargs.get('reason')
        
        # get data
        data = kwargs.get('data')
        if data is not None:
            if isinstance(data, dict):
                data = to_json(data)
            if isinstance(data, str):
                data = data.encode('utf-8')
            data = gzip.compress(data)
            headers['Content-Encoding'] = 'gzip'
            headers['Content-Type'] = 'application/json'

        # check if global rate limited
        if not self.global_event.is_set():
            await self.global_event.wait()

        # open http request with retries
        async with HoldableLock(lock) as hold_lock:
            for tries in range(self.retries):
                async with self.session.request(method, endpoint, headers=headers, data=data) as resp:

                    # get response and header data
                    data = await resp.text(encoding='utf-8')
                    if 'application/json' in resp.headers['content-type']:
                        data = from_json(data)
                    remaining = resp.headers.get('X-Ratelimit-Remaining', 0)

                    # check if route should be rate limited
                    if remaining == '0' and resp.status != 429:
                        hold_lock.hold()
                        delay = int(resp.headers.get('X-Ratelimit-Reset')) - time.time()
                        self.loop.call_later(delay, lock.release)

                    # check if route IS rate limited
                    elif resp.status == 429:
                        with GlobalLock(self.global_event, data.get('global', False)):

                            # wait for rate limit delay delay
                            retry_after = data.get('retry-after', 0)
                            await asyncio.sleep(retry_after / 1000.0, loop=self.loop)

                        # retry request
                        continue

                    # return response data
                    if 300 > resp.status >= 200:
                        return data or None

                    # forbidden path
                    elif resp.status == 403:
                        raise Exception(f"Forbidden: {method} {endpoint}")

                    # path not found
                    elif resp.status == 404:
                        raise Exception(f"Not Found: {method} {endpoint}")

                    # service is down, wait a bit and retry later
                    elif resp.status in (500, 502):
                        await asyncio.sleep(1 + tries * 2, loop=self.loop)
                        continue

                    # unknown http error
                    else:
                        raise Exception(f"HTTP Error: {resp.status} {method} {endpoint}")
=======
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
                    delta = utils._parse_ratelimit_header(resp)
                    throttle.delay()
                    self.loop.call_later(delta, self.lock.release)

                if resp.status >= 400:
                    raise RuntimeError(f"HTTP Error {resp.status}: {resp.reason}")

                if 200 <= resp.status < 300:
                    return data






>>>>>>> e6938cd81dad3fa86c3c4033a988ea6fc18a6f6c

        # retries have been exhausted
        raise Exception(f"Failed HTTP Request: {resp.status} {method} {endpoint}")

