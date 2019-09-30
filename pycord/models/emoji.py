

from .core import Snowflake, Serializable
from ..models.role import Role
from ..utils import Collection


class Emoji(Snowflake, Serializable):
    __slots__ = ('guild', 'id', 'name', 'roles', 'client', 'require_colons', 'managed')

    def __init__(self, guild, data=None):
        if data is None:
            data = {}
        self.guild = guild
        self.client = guild.client
        self.id = int(data.get('id', 0))
        self.name = data.get('name', '')
        self.require_colons = bool(data.get('require_colons', False))
        self.managed = bool(data.get('managed', False))
        self.roles = Collection(Role)
        self.from_dict(data)

    def from_dict(self, data):
        self.id = int(data.get('id', 0))
        self.name = data.get('name')

        for role in data.get('roles', []):
            if role:
                if self.guild.roles.has(role):
                    rolee = self.guild.roles.get(role)
                    self.roles.add(rolee)

    def delete(self, reason=None):
        return self.client.api.delete_custom_emoji(self.guild, self, reason)
