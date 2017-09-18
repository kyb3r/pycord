from .core import Snowflake, Serializable

class Role(Snowflake, Serializable):
  __slots__ = ('guild')

  def __init__(self, guild, data={}):
    self.guild = guild
    self.from_dict(data)
    self.id = int(data.get('id', 0))

#TODO: implement other attributes