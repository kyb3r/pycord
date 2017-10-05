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

from ..models.core import Snowflake, Sendable, Serializable

TEXTCHANNEL = 0
DMCHANNEL = 1
VOICECHANNEL = 2
GROUPDMCHANNEL = 3
CATEGORYCHANNEL = 4

GUILD_CHANNELS = (TEXTCHANNEL, VOICECHANNEL, CATEGORYCHANNEL)
DM_CHANNELS = (GROUPDMCHANNEL, DMCHANNEL)


class Channel(Snowflake, Serializable):
    __slots__ = ('name', 'position',
                 'guild', 'type',
                 'permission_overwrites')


class TextChannel(Sendable, Channel):
    __slots__ = ("topic", "parent")

    def __init__(self, guild, data):
        self.guild = guild
        self.client = self.guild.client
        self.parent = self.client.channels.get(int(data.get("parent_id", 0) or 0))
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
        self.guild = guild
        self.client = self.guild.client
        self.parent = self.client.channels.get(int(data.get("parent_id", 0) or 0))
        self.from_dict(data)

    def __repr__(self):
        return "<VoiceChannel name='{0.name}' id={0.id} bitrate={0.bitrate} limit={0.user_limit}>".format(self)


class CategoryChannel(Channel):
    __slots__ = ('name', 'position', 'guild')

    def __init__(self, guild, data):
        self.guild = guild
        self.client = self.guild.client
        self.parent = self.client.channels.get(int(data.get("parent_id", 0) or 0))
        self.from_dict(data)


class DMGroupChannel(Channel, Sendable):
    __slots__ = ('recipients', 'icon', 'owner')

    def __init__(self, client, data):
        self.client = client
        self.owner = self.client.users.get(int(data.get("owner_id", 0)))
        self.name = None
        self.from_dict(data)
        self.recipients = [self.client.users.get(int(user["id"])) for user in data.get("recipients", ())]

    def trigger_typing(self):
        return self.client.http.send_typing(self)


class DMChannel(Channel, Sendable):
    def __init__(self, client, data):
        self.client = client
        self.parent = self.client.channels.get(int(data.get("parent_id", 0) or 0))
        self.from_dict(data)

    def trigger_typing(self):
        return self.client.http.send_typing(self)
