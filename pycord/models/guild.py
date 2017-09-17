from .core import Snowflake, Serializable
from .user import Member
from .emoji import Emoji

class Guild(Snowflake, Serializable):

    __slots__ = (
        'afk_timeout', 'afk_channel', '_members', '_channels', 'icon',
        'name', 'id', 'unavailable', 'name', 'region',
        'default_role', '_roles', 'member_count', 'large',
        'owner_id', 'mfa_level', '_emojis', 'features',
        'verification_level', 'explicit_content_filter', 'splash',
        )

    def __init__(self, data, state):
        self._channels = {}
        self._members = {}
        self._state = state
        self.from_data(data)

    def from_data(self, data):
        self.name = data.get('name')
        self.region = data.get('region')
        self.verification_level = data.get('verification_level')
        self.explicit_content_filter = data.get('explicit_content_filter', False)
        self.afk_timeout = data.get('afk_timeout')
        self.icon = data.get('icon')
        self.unavailable = data.get('unavailable', False)
        self.id = int(data['id'])
        # self.roles = [Role(r, self) for r in data.get('roles', [])]
        self.mfa_level = data.get('mfa_level')
        self.features = data.get('features', [])
        self.splash = data.get('splash')

        self.emojis = {}
        for e in data.get('emojis',[]):
            e = Emoji(e)
            self.emojis[e.id] = e
            self._state.add_emoji(e)

        for m in data.get('members', []):
            member = Member(m, self, self._state)
            self.add_member(member)

    def add_member(self, member):
        self._members[member.id] = member

    def from_dict(self):
        pass 



