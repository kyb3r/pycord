

from ..models.core import Snowflake, Serializable
from ..models.perms import Permissions


class Role(Snowflake, Serializable):
    __slots__ = (
        'guild', 'id', 'color', 'pinned', 'position',
        'managed', 'mentionable', 'permissions', 'name',
        'colour', 'perms'
    )

    def __init__(self, guild, data):
        if data is None:
            data = {}
        self.guild = guild
        self.from_dict(data)
        self.id = int(data.get('id', 0))

    def from_dict(self, data):
        self.name = data.get('name')
        self.color = data.get('color')
        self.colour = self.color
        self.pinned = data.get('hoist')
        self.position = data.get('position')
        self.managed = data.get('managed')
        self.mentionable = data.get('mentionable')
        perms = data.get('permissions')
        self.perms = Permissions(perms)

    def __str__(self):
        return self.name

    @property
    def mention(self):
        return '<@&{.id}>'.format(self)

#  TODO: implement other attributes
