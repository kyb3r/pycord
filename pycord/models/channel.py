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


class ChannelType:
    Text = 0
    Dm = 1
    Voice = 2
    GroupDm = 3
    Category = 4


class Channel(Snowflake):
    Type = ChannelType


class TextChannel(Channel, Sendable, Serializable):
  
    __slots__ = ('name', 'position', 'guild', 'client')

    def __init__(self, guild, data):
        self.guild = guild
        self.from_dict(data)
        self.id = int(data.get('id', 0))

    def __str__(self):
        return self.name

    # TODO: add permission overwrites

    async def send(self, content:str=None, **kwargs):
        api = self.guild.client.api
        kwargs['content'] = str(content)
        return await api.send_message(self, **kwargs)

    async def trigger_typing(self):
        pass


class VoiceChannel(Channel, Serializable):
    __slots__ = ('name', 'position', 'guild', 'client')

    def __init__(self, guild, data):
        self.guild = guild
        self.from_dict(data)
        self.id = int(data.get('id', 0))
