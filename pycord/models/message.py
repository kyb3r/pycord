

class Message:
    def __init__(self, data, state):
        self.state = state
        self.from_data(data)

    def from_data(self, data):
        self.content = data['content']
        self.id = data['id']
        self.channel = self.state.get_channel(data['channel'])
        self.author = self.state.get_user(data['author']['id'])

#todo