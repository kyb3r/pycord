'''
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
'''


import asyncio
import traceback
from pycord.utils import Emitter
from pycord.models import ClientUser
from pycord.utils import Collection
from pycord.utils import get_event_loop
from pycord.api import HttpClient, ShardConnection
from pycord.models import Channel, Guild, Message, User
from collections import defaultdict
import time
import shlex


class Client(Emitter):
    def __init__(self, shard_count=-1, prefixes='py.'):
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
        self.messages = Collection(Message, maxlen=2500)
        self.commands = {}
        self.prefixes = prefixes if isinstance(prefixes, list) else [prefixes]  

    def __del__(self):
        if self.is_bot:
            self.close()

    async def _close(self):
        for shard in self.shards:
            await shard.close()
        self.running.set()

    def close(self):
        self.loop.run_until_complete(self._close())

    async def start(self, token, bot):
        self.is_bot = bot
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

    def login(self, token, bot=True):
        self._boot_up_time = time.time()
        try:
            self.loop.run_until_complete(self.start(token, bot))
        except KeyboardInterrupt:
            pass
        except Exception as err:
            traceback.print_exc()
        finally:
            self.close()

    async def on_error(self, error):
        '''Default error handler for events'''
        traceback.print_exc()

    async def on_command_error(self, error):
        traceback.print_exc()

    async def on_message(self, message):
        await self.process_commands(message)

    async def process_commands(self, msg):
        context = self.get_command_context(msg)
        if context is None:
            return
        msg, callback, alias = context
        content = msg.content[len(alias):]
        args = shlex.split(content)
        try:
            await callback(msg, *args)
        except Exception as e:
            await self.emit('command_error', e)

    def get_prefix(self, content):
        for prefix in self.prefixes:
            if content.startswith(prefix):
                return prefix

    def get_callback(self, content, prefix):
        for command in self.commands:
            for alias in command:
                if content.startswith(prefix + alias):
                    return self.commands[command], alias

    def get_command_context(self, msg):
        content = msg.content
        prefix = self.get_prefix(content)
        command, alias = self.get_callback(content, prefix)
        return msg, command, prefix + alias
        
    def add_command(self, name, aliases, callback):
        aliases = tuple([name] + aliases)
        for key in self.commands:
            if any(x in key for x in aliases):
                raise ValueError(f'One of {aliases} is already an existing command')
        self.commands[aliases] = callback

    def command(self, callback=None,  *, name=None, aliases=[]):
        if asyncio.iscoroutinefunction(callback):
            name = name or callback.__name__
            self.add_command(name, aliases, callback)
        else:
            def wrapper(coro):
                if not asyncio.iscoroutinefunction(coro):
                    raise RuntimeWarning(f'Callback is not a coroutine!')
                self.add_command(name or coro.__name__, aliases, coro)
                return coro
            return wrapper

