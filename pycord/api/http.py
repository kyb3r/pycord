import asyncio
import aiohttp


class HttpClient:
    def __init__(self, loop=None, connector=None):
        self.loop = loop or asyncio.get_event_loop()
        self.connector = connector
        self.session = aiohttp.ClientSession(loop=self.loop, connector=connector)
        self.token = None
        self.is_bot = True
        self.bucket_locks = weakref.WeakValueDictionary()
        self.global_lock = asyncio.Event()
        self.global_lock.set()

    async def request(self, method, route, **kwargs):
        pass


