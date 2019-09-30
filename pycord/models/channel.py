

from ..models.core import Snowflake, Serializable
from abc import ABC
from .embed import Embed

TEXTCHANNEL = 0
DMCHANNEL = 1
VOICECHANNEL = 2
GROUPDMCHANNEL = 3
CATEGORYCHANNEL = 4

GUILD_CHANNELS = (TEXTCHANNEL, VOICECHANNEL, CATEGORYCHANNEL)
DM_CHANNELS = (GROUPDMCHANNEL, DMCHANNEL)


class Sendable:
    """ Base class for objects that can send messages """

    async def send(self, content=None, *, embed=None, tts=False):
        if isinstance(embed, Embed):
            embed = embed.to_dict()
        return await self.client.api.send_message(self, content=content, embed=embed, tts=tts)

    async def trigger_typing(self):
        return await self.client.api.trigger_typing(self)


class Channel(Snowflake):

    def from_dict(self, data):
        for attr in data:
            if 'id' in attr:
                try:
                    setattr(self, attr, int(data[attr]))
                except TypeError:
                    setattr(self, attr, data[attr])
            else:
                setattr(self, attr, data[attr])


class TextChannel(Sendable, Channel):
    __slots__ = ("topic", "parent", 'name', 'position',
                 'guild', 'type',
                 'permission_overwrites', 'id')

    def __init__(self, guild, data):
        self.type = TEXTCHANNEL
        self.guild = guild
        self.client = self.guild.client
        self.parent = self.client.channels.get(int(data.get("parent_id") or 0))
        self.from_dict(data)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<TextChannel name='{0.name}' id={0.id}>".format(self)

    def trigger_typing(self):
        return self.client.http.send_typing(self)


class VoiceChannel(Channel):
    __slots__ = ('bitrate', 'user_limit', 'parent')

    def __init__(self, guild, data):
        self.type = VOICECHANNEL
        self.guild = guild
        self.client = self.guild.client
        self.parent = self.client.channels.get(int(data.get("parent_id", 0) or 0))
        self.from_dict(data)

    def __repr__(self):
        return "<VoiceChannel name='{0.name}' id={0.id} bitrate={0.bitrate} limit={0.user_limit}>".format(self)


class CategoryChannel(Channel):
    __slots__ = ('name', 'position', 'guild')

    def __init__(self, guild, data):
        self.type = CATEGORYCHANNEL
        self.guild = guild
        self.client = self.guild.client
        self.parent = self.client.channels.get(int(data.get("parent_id", 0) or 0))
        self.from_dict(data)

    def __str__(self):
        return self.name


class DMGroupChannel(Channel, Sendable):
    __slots__ = ('recipients', 'icon', 'owner')

    def __init__(self, client, data):
        self.type = GROUPDMCHANNEL
        self.client = client
        self.owner = self.client.users.get(int(data.get("owner_id", 0)))
        self.name = None
        self.from_dict(data)
        self.recipients = [self.client.users.get(int(user["id"])) for user in data.get("recipients", ())]

    def trigger_typing(self):
        return self.client.http.send_typing(self)


class DMChannel(Channel, Sendable):
    def __init__(self, client, data):
        self.type = DMCHANNEL
        self.client = client
        self.parent = self.client.channels.get(int(data.get("parent_id", 0) or 0))
        self.from_dict(data)

    def trigger_typing(self):
        return self.client.http.send_typing(self)
