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

from abc import ABC, abstractmethod
from itertools import chain
from .message import Message

from ..utils import id_to_time

class Snowflake(ABC):
    """ Base Discord Object : everything will probably inherit from this """
    __slots__ = ('id',)

    @property
    def created_at(self):
        _id = getattr(self, 'id', None)
        if not _id:
            raise AttributeError("id is not set!")
        return id_to_time(int(_id))

class Sendable(ABC):
    """ Base class for objects that can send messages """
    __slots__ = ()

    async def send(self, content=None, **kwargs):
        data = await self.client.api.send_message(self, content=content, **kwargs)
        message = Message(self.client, data)
        return message

    async def fsend(self, content=None, **kwargs):
        try:
            return await self.send(content, **kwargs)
        except:
            return None

    @abstractmethod
    async def trigger_typing(self):
        return await self.client.api.trigger_typing(self)

class Serializable(ABC):
    """ Anything that can go to and from a dict """
    __slots__ = ()

    @abstractmethod
    def from_dict(self, data):
        return NotImplemented

    def to_dict(self):
        return NotImplemented
