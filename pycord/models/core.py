from ..utils import id_to_time
from abc import ABC, abstractmethod

class Snowflake(ABC):
    ''' Base Discord Object : everything will probably inherit from this '''
    __slots__ = ('id')

    @property
    def created_at(self):
        _id = getattr(self, 'id', None)
        if not _id:
            raise AttributeError("id is not set!")
        return id_to_time(int(_id))

class Sendable(ABC):
    ''' Base class for objects that can send messages '''
    __slots__ = ()

    @abstractmethod
    async def send(self, **kwargs):
        pass

    @abstractmethod
    async def trigger_typing(self):
        pass

class Serializable(ABC):
    ''' Anything that can go to and from a dict '''
    __slots__ = ()

    @abstractmethod
    def from_dict(self, data):
        pass

    def to_dict(self):
        d = {key: getattr(self, key, None) for key in self.__slots__}
        return {key: value for key, value in d.items() if value is not None}