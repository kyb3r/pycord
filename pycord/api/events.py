from ..utils import json
from ..models import ClientUser, Guild
from collections import deque

class EventHandler:
    def __init__(self, client):
        self.client = client
        self.loop = client.loop
        self.http = client.api

    def reset(self):
        self.user = None
        self.guilds = {}
        self.users = {}
        self.emojis = {}
        self.messages = deque(maxlen=2000)

    def add_emoji(self, emoji):
        self.emojis[emoji.id] = emoji

    def get_guild(self, id):
        return self.guilds.get(id)

    def add_guild_from_data(self, data):
        guild = Guild(data, self)
        self.guilds[guild.id] = guild

    def add_guild(self, guild):
        self.guilds[guild.id] = guild

    async def handle_ready(self, data):
        self.reset()

        self.user = ClientUser(data['user'], self)
        for guild in data['guilds']:
            self.add_guild_from_data(guild)

        await self.client.emit('ready')

        # have to somehow block the self.client.emit until all the guilds are parsed

    async def handle_message_create(self, data):
        msg = Message(data, self)
        await self.client.emit('message', msg)

    async def handle_guild_create(self, data):
        print('created guilds')
        guild = self.guilds.get(int(data['id']))
        if guild:
            guild.from_data(data)
            self.add_guild(guild)
        else:
            self.add_guild_from_data(data)

        await self.client.emit('guild_create')
