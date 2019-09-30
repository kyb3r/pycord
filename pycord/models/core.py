

from abc import ABC, abstractmethod
from itertools import chain
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


class Serializable(ABC):
    """ Anything that can go to and from a dict """
    __slots__ = ()

    @abstractmethod
    def from_dict(self, data):
        return NotImplemented

    def to_dict(self):
        return NotImplemented
