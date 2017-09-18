from .core import Snowflake, Sendable, Serializable

class ChannelType:
  Text = 0
  Dm = 1
  Voice = 2
  GroupDm = 3
  Category = 4

class Channel(Snowflake):
  Type = ChannelType

class TextChannel(Channel, Sendable, Serializable):
  __slots__ = ('name', 'position', 'guild', 'client')

  def __init__(self, guild, data):
    self.guild = guild
    self.from_dict(data)
    self.id = int(data.get('id', 0))

  async def send(self, content=None, **kwargs):
      api = self.guild.client.api
      kwargs['content'] = content
      return await api.send_message(self, **kwargs)

  async def trigger_typing(self):
      pass

class VoiceChannel(Channel, Serializable):
  __slots__ = ('name', 'position', 'guild', 'client')

  def __init__(self, guild, data):
    self.guild = guild
    self.from_dict(data)
    self.id = int(data.get('id', 0))