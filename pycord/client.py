import inspect
import time
import traceback
from collections import deque

import anyio
import asks
import sys

import sniffio

from .api import HttpClient, ShardConnection, Webhook
from .models import Channel, Guild, User
from .utils import Collection
from .utils import Emitter
from .utils.commands import Command, CommandCollection, Context


class Client(Emitter):
    """
    Represents a client that connects to Discord.

    This class is the core of the library, with all functionality
    revolving around it.

    Parameters
    ----------
    shard_count : Optional[int]
        The amount of shards to use, this will be automatically set
        using the bot ws gateway endpoint if not provided.
    message_cache_max : Optional[int]
        The maximum number of messages to store in the internal deque
        cache. Defaults to 2500 if not provided.
    prefixes : optional[str, list]
        The prefixes to use for commands. Can either be a list or a
        single prefix. Defaults to 'py.' if not provided.

    Attributes
    ----------
    token : str
        The bot token provided by the login method.
    is_bot : bool
        Specifies whether or not the client is a bot.
    shards : list
        Stores the client's ShardConnections (ws) indexed by id
    users : collection
        Stores all user objects that the client can see
    guilds : collection
        Stores all the guild objects the client is a part of currently.
    channels : collection
        Stores all the channel objects that the client can see.
    messages : collection
        A deque cache that stores the last x amount of messages
        specified by the ``message_cache_max`` parameter.
    commands : collection
        A special collection that stores all registered commands
    prefixes : list
        Contains a list of prefixes that a command may be used with
    session
        An asks.Session that is for public use, this is different from
        the internal session the HttpClient uses.

    """

    def __init__(self, library, shard_count=-1, prefixes='py.', message_cache_max=2500, **kwargs):
        super().__init__()
        sniffio.current_async_library_cvar.set(library)
        self.token = ''
        self.is_bot = True
        self._boot_up_time = None
        self.running = anyio.create_event()
        self.api = HttpClient(self)
        self.session = asks.Session()  # public session
        self.shards = [] if shard_count < 1 else list(range(shard_count))
        self.users = Collection(User)
        self.guilds = Collection(Guild)
        self.channels = Collection(Channel)
        self.messages = deque(maxlen=message_cache_max)
        self.commands = CommandCollection(self)
        self.webhooks = Collection(Webhook, indexor='name')
        self.prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
        self._nonces = dict()
        self.user = None

    def __del__(self):
        if self.is_bot:
            self.close()

    def wait_for_nonce(self, nonce):
        event = anyio.create_event()
        self._nonces[str(nonce)] = event
        return event.wait()

    async def _close(self):
        for shard in self.shards:
            await shard.close()
        await self.running.set()

    async def close(self):
        await self._close()

    async def start(self, token, bot):
        self.token = self.api.token = token
        self.is_bot = bot

        # get gateway info
        endpoint = '/gateway'
        if self.is_bot:
            endpoint += '/bot'
        info = await self.api.get(endpoint)

        url = info.get('url')

        # get amount of shards
        shard_count = info.get('shards', 1)
        if len(self.shards) < 1:
            self.shards = list(range(shard_count))
        else:
            shard_count = len(self.shards)

        # spawn shard connections
        async with anyio.create_task_group() as nursery:
            for shard_id in range(shard_count):
                shard = ShardConnection(self, shard_id, shard_count)
                self.shards[shard_id] = shard
                await nursery.spawn(shard.start, url)

        # wait for client to stop running
        await self.running.wait()

    async def login(self, token, bot=True):
        self._boot_up_time = time.time()
        try:
            await self.start(token, bot)
        except KeyboardInterrupt:
            pass
        finally:
            await self.close()

    async def on_error(self, error):
        """Default error handler for events"""
        print('Error caught for the on_error event:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__)

    async def on_command_error(self, error):
        traceback.print_exception(type(error), error, error.__traceback__)

    async def on_message(self, message):
        await self.process_commands(message)

    async def process_commands(self, msg):
        context = Context(self, msg)
        await context.invoke()

    def cmd(self, name=None, *, callback=None, aliases=[]):
        if isinstance(aliases, str):
            aliases = [aliases]
        if inspect.iscoroutinefunction(callback):
            name = name or callback.__name__
            cmd = Command(name=name, callback=callback, aliases=aliases)
            self.commands.add(cmd)
        else:
            def wrapper(coro):
                if not inspect.iscoroutinefunction(coro):
                    raise RuntimeWarning('Callback is not a coroutine!')
                cmd = Command(name=name or coro.__name__, callback=coro, aliases=aliases)
                self.commands.add(cmd)
                return cmd

            return wrapper

    def add_webhook(self, name, url, **fields):
        '''Register a webhook to the client.

        Example:
            client.register_webhook('test', url)
            await client.webhooks.get('test').send('hello', embeds=em)
        '''
        hook = Webhook(url=url, name=name, **fields)
        self.webhooks.add(hook)
