from .core import Snowflake, Sendable, Serializable



class User(Snowflake, Sendable, Serializable):

    __slots__ = (
        'username', 'avatar','id',
        'discriminator', 'bot', 'verified'
        )

    def __init__(self, data={}):
        self.from_dict(data)

    def from_dict(self, data):
        for key in self.__slots__:
            if key in data and data[key] is not None:
                setattr(self, key, data[key])

    async def send(self, **kwargs):
        pass

    async def trigger_typing(self):
        pass


class ClientUser(User):

    __slots__ = (
        'email', 'mfa_enabled','username', 'avatar',
        'discriminator', 'bot', 'verified','id'
        )

    def __init__(self, data={}, state=None):
        super().__init__()
        self._state = state

        for key in self.__slots__:
            if key in data:
                setattr(self, key, data[key])



class Member(User):

    __slots__ = (
        '_roles', 'username', 'avatar','id',
        'discriminator', 'bot', 'verified',
        'guild', 'nick'
        )

    def __init__(self, data, guild, state):
        super().__init__()
        self._state = state
        self.guild = guild
        self.id = int(data['user'].get('id'))
        self.bot = data.get('bot')
        self.verified = data.get('verified')
        self.from_data(data)

    def from_data(self, data):
        self.username = data.get('username')
        self.avatar = data.get('avatar')
        self.discriminator = data.get('discriminator')
        if data.get('nick'):
            self.nick = data.get('nick')


# not done yet


