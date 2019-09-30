from ..models.core import Snowflake, Serializable
from .channel import Sendable
from ..models.role import Role
from ..utils import Collection


class User(Snowflake, Sendable, Serializable):

    def __init__(self, client, data=None):
        if data is None:
            data = {}
        self.from_dict(data)
        self.id = int(data.get('id', 0))

    def from_dict(self, data):
        self.name = data.get('username')
        self.avatar = data.get('avatar')
        self.discrim = data.get('discriminator')
        self.bot = data.get('bot')
        self.verified = data.get('verified')

    def __str__(self):
        return '{0.name}#{0.discrim}'.format(self)

    def __eq__(self, other):
        return isinstance(other, __class__) and other.id == self.id

    @property
    def mention(self):
        return '<@{.id}>'.format(self)

    async def send(self, **kwargs):
        pass

    async def trigger_typing(self):
        pass


class ClientUser(User):

    def __init__(self, client, data):
        super().__init__(client, data)
        self.from_dict(data)

    def from_dict(self, data):
        data = data['user']
        self.id = int(data.get('id', 0))
        self.email = data.get('email')
        self.name = data.get('username')
        self.avatar = data.get('avatar')
        self.discrim = data.get('discriminator')
        self.bot = data.get('bot')
        self.verified = data.get('verified')
        self.mfa_enabled = data.get('mfa_enabled')
        self.email = data.get('email')


class Member(Snowflake, Serializable):

    def __init__(self, client, guild, user, data={}):
        super().__init__()
        self.client = client
        self.guild = guild
        self.user = user
        self.roles = Collection(Role)
        self.from_dict(data)

    def __str__(self):
        return str(self.user)

    @property
    def mention(self):
        return self.user.mention

    @property
    def id(self):
        return self.user.id

    @property
    def name(self):
        return self.user.name

    @property
    def avatar(self):
        return self.user.avatar

    @property
    def discrim(self):
        return self.user.discrim

    @property
    def bot(self):
        return self.user.bot

    @property
    def verified(self):
        return self.user.verified

    def from_dict(self, data):
        self.nick = data.get('nick')
        self.status = 'offline'

        if self.guild:
            for role in data.get('roles', []):
                role = self.guild.roles.get(int(role))
                if role:
                    self.roles.add(role)

    async def kick(self, reason=None):
        await self.client.api.kick(self, self.guild, reason)

    async def ban(self, reason=None, delete_message_days=1):
        await self.client.api.ban(self, self.guild, delete_message_days, reason)

    async def unban(self, reason=None):
        await self.client.api.unban(self, self.guild, reason=reason)

# not done yet
