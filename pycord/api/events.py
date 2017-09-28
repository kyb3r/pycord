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

from ..models import ClientUser, Guild, Message
from ..utils import json
from collections import deque
import time

class EventHandler:
    def __init__(self, shard):
        self.shard = shard
        self.client = shard.client
        self.api = self.client.api
        self.emitted_ready = False

    async def handle_ready(self, data):
        self.client.user = ClientUser(self.client, data)
        for guild in data['guilds']:
            self.client.guilds.add(Guild(self.client, guild))

        if not self.client.is_bot and not self.emitted_ready:
            bootup = time.time()-self.client._boot_up_time
            await self.client.emit('ready', bootup)
            self.emitted_ready = True

    async def handle_message_create(self, data):
        message = Message(self.client, data)
        self.client.messages.add(message)
        await self.client.emit('message', message)

    async def handle_guild_create(self, data):
        guild = self.client.guilds.get(int(data['id']))
        if guild:
            guild.from_dict(data)
        else:
            self.client.guilds.add(Guild(self.client, data))

        if not self.emitted_ready:
            if len([None for g in self.client.guilds if g.unavailable]) == 0:
                bootup = time.time()-self.client._boot_up_time
                await self.client.emit('ready', bootup)

    async def handle_member_join(self, data):
        pass

