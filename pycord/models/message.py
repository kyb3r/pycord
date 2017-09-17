from .core import Snowflake, Serializable

class Message(Snowflake, Serializable):
    __slots__ = (
        'client', 'guild', 'content', 
        'edited', 'channel', 'author', 'members'
    )

    def __init__(self, client, data={}):
        self.client = client
        self.from_dict(data)

    def from_dict(self, data):
        self.id = int(data.get('id'))
        self.content = data.get('content')
        
        channel_id = int(data['channel_id'], 0)
        self.channel = self.client.channels.get(channel_id)

        if 'author' in data:
            author_id = int(data['author']['id'])
            self.author = self.client.users.get(author_id)

#todo