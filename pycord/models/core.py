from abc import ABC, abstractmethod



class Snowflake(ABC):
    '''Everything is probably inherited from this'''
    __slots__ - ()

    attributes = ('id', 'created_at')

    @abstractmethod
    def created_at(self):
        pass

    @classmethod
    def __subclasshook__(cls, klass):
        if cls is Snowflake:
            for attr in cls.attributes:
                for base in klass.__mro__:
                    if attr in base.__dict__:
                        break
                else:
                    return NotImplemented
            return True
        else:
            return NotImplemented


class User(ABC):

    __slots__ = ()

    attributes = (
        'nickname', 'name', 'mention', 
        'avatar', 'discrim', 'is_bot'
        )

    @property
    @abstractmethod
    def mention(self):
        pass

    @classmethod
    def __subclasshook__(cls, klass):
        if cls is User:
            if Snowflake.__subclasshook__(klass) is NotImplemented:
                return NotImplemented
            for attr in cls.attributes:
                for base in klass.__mro__:
                    if attr in base.__dict__:
                        break
                else:
                    return NotImplemented
            return True
        return NotImplemented




class Sendable(ABC):
    '''Base class that TextChannels, Users and PrivateChannels inherit from'''

    __slots__ = ()
    
    def send(self, content=None, embed=None, file=None, tts=False):
        pass

    def trigger_typing(self):
        pass