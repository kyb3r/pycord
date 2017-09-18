import asyncio
import traceback
from .utils import Emitter
from .models import ClientUser
from .utils import Collection
from .utils import get_event_loop
from .api import HttpClient, ShardConnection
from .models import Channel, Guild, Message, User


class Client(Emitter):
    def __init__(self, shard_count=-1):
        super().__init__()
        self.token = ''
        self.is_bot = True
        self.loop = get_event_loop()
        self.running = asyncio.Event()
        self.api = HttpClient(self.loop)
        self.shards = [] if shard_count < 1 else list(range(shard_count))
        self.users = Collection(User)
        self.guilds = Collection(Guild)
        self.channels = Collection(Channel)
        self.messages = Collection(Message)

    def __del__(self):
        if self.is_bot:
            self.close()

    async def _close(self):
        for shard in self.shards:
            await shard.close()
        self.running.set()

    def close(self):
        self.loop.run_until_complete(self._close())

    async def start(self, token, bot=True):
        self.is_bot = True
        self.token = self.api.token = token

        # get gateway info
        endpoint = '/gateway'
        if self.is_bot:
            endpoint += '/bot'
        info = await self.api.get(endpoint)
        url = info.get('url')

        # get amouont of shards
        shard_count = info.get('shards', 1)
        if len(self.shards) < 1:
            self.shards = list(range(shard_count))
        else:
            shard_count = len(self.shards)

        # spawn shard connections
        for shard_id in range(shard_count):
            shard = ShardConnection(self, shard_id, shard_count)
            self.shards[shard_id] = shard
            self.loop.create_task(shard.start(url))

        # wait for client to stop running
        await self.running.wait()

    def login(self, *args, **kwargs):
        try:
            self.loop.run_until_complete(self.start(*args, **kwargs))
        except KeyboardInterrupt:
            pass
        except Exception as err:
            traceback.print_exc()
        self.close()