import pycord
import datetime

class MyBot(pycord.Client):
    '''
    Example of dynamic event registration
    ------------------------------------
    on_{event} methods are automatically called to make event 
    registration easier if you decide to make a subclass
    of `pycord.Client`. Otherwise you can use the `self.on` method
    and pass in a callback to register it for the specified event.
    '''
    def __init__(self):
        super().__init__()
        self.on('message', self.message_handler)

    async def message_handler(self, msg):
        print('This event was registered in __init__')

    async def on_message(self, msg):
        print('This event is called automatically')

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        print('This event is called automatically')


if __name__ == '__main__':
    client = MyBot()
    client.login('token')
