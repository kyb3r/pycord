"""
MIT License

Copyright (c) 2017 verixx / king1600

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import inspect
import time
import traceback

import asks
import multio

from .api import HttpClient, ShardConnection, Webhook
from .models import Channel, Guild, Message, User
from .utils import Collection
from .utils import Emitter
from .utils.commands import Command, CommandCollection, Context

class Client(Emitter):
    '''
    Represents a client that connects to Discord.

    This class is the core of the library, with all functionality
    revolving around it.

    Parameters
    ----------
    shard_count : Optional[int]
        The amount of shards to use, this will be automatically set 
        using the bot ws gateway endpoint if not provided.
    lib : Optional[str]
        The async library to use, supports either 'trio' or 'curio',
        defaults to 'trio' if not provided.
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
        
    '''

    def __init__(self, shard_count=-1, prefixes='py.', message_cache_max=2500, lib='trio'):
        super().__init__()
        self.async_init(lib)
        self.token = ''
        self.is_bot = True
        self._boot_up_time = None
        self.running = multio.Event()
        self.api = HttpClient(self)
        self.session = asks.Session()  # public session
        self.shards = [] if shard_count < 1 else list(range(shard_count))
        self.users = Collection(User)
        self.guilds = Collection(Guild)
        self.channels = Collection(Channel)
        self.messages = Collection(Message, maxlen=message_cache_max)
        self.commands = CommandCollection(self)
        self.webhooks = Collection(Webhook, index='name')
        self.prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
        
    def __del__(self):
        if self.is_bot:
            self.close()

    def async_init(self, lib):
        multio.init(lib)
        asks.init(lib)

    async def _close(self):
        for shard in self.shards:
            await shard.close()
        await self.running.set()

    def close(self):
        multio.run(self._close)

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
        async with multio.asynclib.task_manager() as nursery:
            for shard_id in range(shard_count):
                shard = ShardConnection(self, shard_id, shard_count)
                self.shards[shard_id] = shard
                await multio.asynclib.spawn(nursery, shard.start, url)

        # wait for client to stop running
        await self.running.wait()

    def login(self, token, bot=True):
        self._boot_up_time = time.time()
        try:
            multio.run(self.start, token, bot)
        finally:
            self.close()

    async def on_error(self, error):
        """Default error handler for events"""
        traceback.print_exc()  # This actually just prints None...
        # error.__traceback__ can be printed however

    async def on_command_error(self, error):
        traceback.print_exc()

    async def on_message(self, message):
        await self.process_commands(message)

    async def process_commands(self, msg):
        context = Context(self, msg)
        await context.invoke()

    def cmd(self, name=None, *, callback=None, aliases=None):
        if aliases is None:
            aliases = []
        if inspect.iscoroutinefunction(callback):
            name = name or callback.__name__
            cmd = Command(self, name=name, callback=callback, aliases=aliases)
            self.commands.add(cmd)
        else:
            def wrapper(coro):
                if not inspect.iscoroutinefunction(coro):
                    raise RuntimeWarning(f'Callback is not a coroutine!')
                cmd = Command(self, name=name or coro.__name__, callback=coro, aliases=aliases)
                self.commands.add(cmd)
                return cmd

            return wrapper

    def register_webhook(self, name, url, **fields):
        '''Register a webhook to the client.

        Example:
            client.register_webhook('test', url)
            await client.webhooks.get('test').send('hello', embeds=em)
        '''
        hook = Webhook(url=url, name=name, **fields)
        self.webhooks.add(hook)
