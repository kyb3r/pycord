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


from ..models.core import Snowflake, Serializable


class Message(Snowflake, Serializable):
    __slots__ = (
        'client', 'guild', 'content', 
        'edited', 'channel', 'author', 'members'
    )

    def __init__(self, client, data=None):
        if data is None:
            data = {}
        self.client = client
        self.guild = None
        self.from_dict(data)

    def from_dict(self, data):
        self.id = int(data.get('id'))
        self.content = data.get('content')
        channel_id = int(data['channel_id'], 0)
        self.channel = self.client.channels.get(channel_id)
        self.guild = self.channel.guild
        if 'author' in data:
            author_id = int(data['author']['id'])
            self.author = self.client.users.get(author_id)

    async def reply(self, content: str=None, **kwargs):
        kwargs['content'] = str(content)
        return await self.client.api.send_message(self.channel, **kwargs)