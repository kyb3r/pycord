import time

import anyio

from ..models import User
from ..models import ClientUser, Guild, Message, DMChannel, DMGroupChannel, DMCHANNEL, GROUPDMCHANNEL


class EventHandler:
    def __init__(self, shard):
        self.shard = shard
        self.client = shard.client
        self.api = self.client.api
        self.ready_event = anyio.create_event()

    async def handle_ready(self, data):
        self.client.user = ClientUser(self.client, data)

        for guild in data['guilds']:
            await self.handle_guild_create(guild)

        for channel in data["private_channels"]:
            if channel["type"] == DMCHANNEL:
                self.client.channels.add(DMChannel(self.client, data))
            elif channel["type"] == GROUPDMCHANNEL:
                self.client.channels.add(DMGroupChannel(self.client, data))

        await self.ready_event.wait()
        bootup = time.time() - self.client._boot_up_time
        await self.client.emit('ready', bootup)

    async def handle_message_create(self, data):
        if not self.ready_event.is_set():
            await self.ready_event.wait()
        message = Message(self.client, data)
        self.client.messages.append(message)
        if message.nonce in self.client._nonces:
            self.client._nonces.pop(message.nonce).set_result(message)
        await self.client.emit('message', message)

    async def handle_guild_create(self, data):
        guild = self.client.guilds.get(int(data['id']))
        if guild:
            guild.from_dict(data)
        else:
            guild = Guild(self.client, data)
            self.client.guilds.add(guild)

        if not any(g.unavailable for g in self.client.guilds):
            await self.ready_event.set()

    async def handle_member_join(self, data):
        '''Handles the event when a member joins a guild.'''
        user = data.get('user')
        if user:
            user_id = int(user['id'])
            if not self.client.users.has(user_id):
                user = User(self.client, user)
                self.client.users.add(user)
            else:
                user = self.client.users.get(user_id)

        # TODO: Check data and add to guild accordingly.

    async def handle_member_update(self, data):
        '''Handles a guild member update (nickname change, role add, etc...)'''
        return NotImplemented

    async def handle_message_update(self, data):
        '''Handles a message edit.'''
        return NotImplemented
