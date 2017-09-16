

class Sendable:
    '''Base class that TextChannels, Users and PrivateChannels inherit from'''

    def send(self, content=None, embed=None, file=None, tts=False):
        pass

    def trigger_typing(self):
        pass