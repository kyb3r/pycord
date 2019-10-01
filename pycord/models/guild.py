from ..models.channel import (Channel, TextChannel, VoiceChannel,
                              CategoryChannel, TEXTCHANNEL, VOICECHANNEL)
from ..models.core import Snowflake, Serializable
from ..models.emoji import Emoji
from ..models.role import Role
from ..models.user import Member, User
from ..utils import Collection


class Game:
    def __init__(self, game):
        self.name = game.get('name')
        self.type = game.get('type')
        # TODO: Enum for type

    def __str__(self):
        types = {
            0: 'Playing',
            1: 'Streaming',
            2: 'Listening to',
            3: 'Watching',
        }
        return f'{types.get(self.type)} {self.name}'


class Guild(Snowflake, Serializable):
    __slots__ = (
        'members', 'channels', 'emojis', 'roles',
        'afk_timeout', 'afk_channel', 'icon',
        'name', 'unavailable', 'name', 'region',
        'default_role', 'member_count', 'large',
        'owner_id', 'mfa_level', 'features', 'client',
        'verification_level', 'explicit_content_filter', 'splash',
        'owner'
    )

    def __init__(self, client, data=None):
        if data is None:
            data = {}
        self.client = client
        self.roles = Collection(Role)
        self.emojis = Collection(Emoji)
        self.members = Collection(Member)
        self.channels = Collection(Channel)
        self.id = int(data.get("id"), 0)
        self.name = None
        self.icon = None
        self.region = None
        self.splash = None
        self.mfa_level = None
        self.features = None
        self.verification_level = None
        self.explicit_content_filter = None
        if not data.get("unavailable", False):
            self.from_dict(data)
        else:
            self.unavailable = True

    def __str__(self):
        return self.name

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
        self.owner_id = int(data.get('owner_id') or 0)

        for channel_data in data.get('channels', []):
            chan_type = channel_data.get('type', 0)
            if chan_type == TEXTCHANNEL:
                channel = TextChannel(self, channel_data)
            elif chan_type == VOICECHANNEL:
                channel = VoiceChannel(self, channel_data)
            else:
                channel = CategoryChannel(self, channel_data)
            self.client.channels.add(channel)
            self.channels.add(channel)

        for role in data.get('roles', []):
            self.roles.add(Role(self, role))

        for emoji in data.get('emojis', []):
            self.emojis.add(Emoji(self, emoji))

        for member in data.get('members', []):
            user = member.get('user')
            if user:
                user_id = int(user['id'])
                if not self.client.users.has(user_id):
                    user = User(self.client, user)
                    self.client.users.add(user)
                else:
                    user = self.client.users.get(user_id)

            self.members.add(Member(self.client, self, user, member))

        for presence in data.get('presences', []):
            member = self.members.get(int(presence['user']['id']))
            if member is None:
                continue
            game = presence.get('game')
            member.game = Game(game) if game else None
            member.status = presence.get('status')
            if not member.bot:
                member.user.status = member.status
                member.user.game = member.game

        self.owner = self.members.get(self.owner_id)

    @property
    def icon_url(self):
        return self.icon_url_as()

    def icon_url_as(self, format='png', size=1024):
        return 'https://cdn.discordapp.com/icons/{0.id}/{0.icon}.{1}?size={2}'.format(self, format, size)

    @property
    def text_channels(self):
        return tuple(filter(lambda x: isinstance(x, TextChannel), self.channels))

    @property
    def voice_channels(self):
        return tuple(filter(lambda x: isinstance(x, VoiceChannel), self.channels))

    def add_member(self, member):
        self.members[member.id] = member
