'''
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
'''


from ..models.core import Snowflake, Sendable, Serializable
from ..models.role import Role
from ..utils import Collection


class User(Snowflake, Sendable, Serializable):

    __slots__ = (
        'username', 'avatar','id','avatar',
        'discriminator', 'bot', 'verified'
        )

    def __init__(self, client, data={}):
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
        return isinstance(other, self) and other.id == self.id

    @property
    def mention(self):
        return f'<@{self.id}>'

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
        self.name = data.get('username')
        self.avatar = data.get('avatar')
        self.discrim = data.get('discriminator')
        self.bot = data.get('bot')
        self.verified = data.get('verified')
        self.mfa_enabled = data.get('mfa_enabled')
        self.email = data.get('email')


class Member(Snowflake, Serializable):

    __slots__ = (
        'roles', 'user', 'guild', 'nick','client'
    )

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

        if self.guild:
            for role in data.get('roles', []):
                role = self.guild._roles.get(int(role))
                if role:
                    self.roles.add(role)

    async def kick(self, reason=None):
        await self.client.api.kick(self, self.guild, reason)

    async def ban(self, reason=None, delete_message_days=1):
        await self.client.api.ban(self, self.guild, delete_message_days, reason)

    async def unban(self, reason=None):
        await self.client.api.unban(self, self.guild, reason=reason)


# not done yet


