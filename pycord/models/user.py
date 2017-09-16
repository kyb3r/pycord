from .core import abstractmethod
from .core import Snowflake, Sendable, Serializable

class User(Snowflake, Sendable, Serializable):
    __slots__ = (
        'nickname', 'name', 'avatar',
        'discrim', 'is_bot', 'verified')

    def __init__(self, data={}):
        self.from_dict(data)

    def from_dict(self, data):
        for key in __class__.__slots__:
            if key in data and data[key] is not None:
                setattr(self, key, data[key])

    async def send(self, **kwargs):
        pass

    async def trigger_typing(self):
        pass