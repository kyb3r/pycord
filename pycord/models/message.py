


from ..models.core import Snowflake, Serializable
from ..models.channel import GUILD_CHANNELS
from ..models.embed import Embed
from ..utils import parse_time


class Message(Snowflake):
    __slots__ = ("guild", "content", "tts", "channel", "author",
                 "mention_everyone", "mentions", "mention_roles",
                 "attachments", "embeds", "channel_id", "timestamp",
                 "edited_timestamp", "pinned", "nonce", "webhook_id",
                 "type", "client", "author_id", "reactions")

    def __init__(self, client, data=None):
        self.client = client
        self.id = int(data['id'])
        self.channel_id = int(data['channel_id'], 0)
        self.channel = self.client.channels.get(self.channel_id)
        if self.channel is None:
            print(self.channel_id)
        self.author_id = author_id = int(data['author']['id'])
        self.author = self.client.users.get(author_id)
        self.guild = self.channel.guild if self.channel and self.channel.type in GUILD_CHANNELS else None
        self.content = data['content']
        self.timestamp = parse_time(data['timestamp'])
        self.edited_timestamp = parse_time(data.get('edited_timestamp'))
        self.tts = data.get("tts", False)
        self.mention_everyone = data["mention_everyone"]
        self.mentions = [self.client.users.get(id["id"]) for id in data["mentions"]]
        if self.guild:
            self.mention_roles = [self.guild._roles[id] for id in data["mention_roles"]]
        else:
            self.mention_roles = None
        self.attachments = data["attachments"]
        self.embeds = [Embed.from_dict(embed) for embed in data["embeds"]]
        self.reactions = data.get("reactions", ())
        self.nonce = data.get("nonce", 0)
        self.pinned = data["pinned"]
        wh_id = data.get("webhook_id")
        if wh_id is not None:
            self.webhook_id = wh_id
        self.type = data.get("type", 0)

    def reply(self, content: str=None, **kwargs):
        return self.channel.send(content, **kwargs)

    def delete(self):
        return self.client.api.delete_message(self.channel, self)




