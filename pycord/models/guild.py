from .role import Role
from .emoji import Emoji
from ..utils import Collection
from .user import Member, User
from .core import Snowflake, Serializable
from .channel import Channel, TextChannel, VoiceChannel

class Guild(Snowflake, Serializable):

    __slots__ = (
        '_members', '_channels', '_emojis', '_roles',
        'afk_timeout', 'afk_channel', 'icon',
        'name', 'id', 'unavailable', 'name', 'region',
        'default_role', 'member_count', 'large',
        'owner_id', 'mfa_level', 'features', 'client',
        'verification_level', 'explicit_content_filter', 'splash',
    )

    def __init__(self, client, data={}):
        self.client = client
        self._roles = Collection(Role)
        self._emojis = Collection(Emoji)
        self._members = Collection(Member)
        self._channels = Collection(Channel)
        self.from_dict(data)

    def from_dict(self, data):
        self.id = int(data.get('id', 0))
        self.name = data.get('name')
        self.icon = data.get('icon')
        self.region = data.get('region')
        self.splash = data.get('splash')
        self.mfa_level = data.get('mfa_level')
        self.features = data.get('features', [])
        self.unavailable = data.get('unavailable', True)
        self.verification_level = data.get('verification_level')
        self.explicit_content_filter = data.get('explicit_content_filter', False)
    
        for role in data.get('roles', []):
            self._roles.add(Role(self, role))

        for emoji in data.get('emojis', []):
            self._emojis.add(Emoji(self, emoji))

        for member in data.get('members', []):
            user = member.get('user')
            if user:
                user_id = int(user['id'])
                if not self.client.users.has(user_id):
                    user = User(self.client, user)
                    self.client.users.add(user)
                else:
                    user = self.client.users.get(user_id)
            self._members.add(Member(self, user, member))

        for channel_data in data.get('channels', []):
            chan_type = channel_data.get('type')
            if chan_type == Channel.Type.Text:
                channel = TextChannel(self, channel_data)
            elif chan_type == Channel.Type.Voice:
                channel = VoiceChannel(self, channel_data)
            else:
                channel = None
            if channel is not None:
                self.client.channels.add(channel)
                self._channels.add(channel)


    def add_member(self, member):
        self._members[member.id] = member


