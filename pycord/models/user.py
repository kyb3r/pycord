from .role import Role
from ..utils import Collection
from .core import Snowflake, Sendable, Serializable

class User(Snowflake, Sendable, Serializable):

    __slots__ = (
        'username', 'avatar','id','avatar',
        'discriminator', 'bot', 'verified'
        )

    def __init__(self, client, data={}):
        self.from_dict(data)
        self.id = int(data.get('id', 0))

    def __str__(self):
        return '{0.username}#{0.discriminator}'.format(self)

    @property
    def mention(self):
        return '<@!{self.id}>'

    async def send(self, **kwargs):
        pass

    async def trigger_typing(self):
        pass


class ClientUser(User):

    __slots__ = (
        'email', 'mfa_enabled','username', 'avatar',
        'id','avatar','discriminator', 'bot', 'verified'
        )

    def __init__(self, client, data):
        self.from_dict(data)

    def from_dict(self, data):
        data = data['user']
        self.id = int(data.get('id', 0))
        self.email = data.get('email')
        self.username = data.get('username')
        self.avatar = data.get('avatar')
        self.discriminator = data.get('discriminator')
        self.bot = data.get('bot')
        self.verified = data.get('verified')
        self.mfa_enabled = data.get('mfa_enabled')
        self.email = data.get('email')


class Member(Snowflake, Serializable):

    __slots__ = (
        '_roles', '_user', 'guild', 'nick',
    )

    def __init__(self, guild, user, data={}):
        super().__init__()
        self.guild = guild
        self._user = user
        self._roles = Collection(Role)
        self.from_dict(data)

    @property
    def username(self):
        return self._user.username

    @property
    def avatar(self):
        return self._user.avatar

    @property
    def discrim(self):
        return self._user.discriminator

    @property
    def bot(self):
        return self._user.bot

    @property
    def verified(self):
        return self._user.verified

    def from_dict(self, data):
        self.nick = data.get('nick')
        self.id = int(data.get('id', 0))

        if self.guild:
            for role in data.get('roles', []):
                role = self.guild._roles.get(int(role))
                if role:
                    self._roles.add(role)

# not done yet


