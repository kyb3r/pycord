import datetime

import pycord
import asyncio


async def message_handler(msg):
    print("This event was registered in __init__ and doesn't have to be part of my client class")


class MyBot(pycord.Client):
    """
    Example of dynamic event registration
    ------------------------------------
    on_{event} methods are automatically called to make event 
    registration easier if you decide to make a subclass
    of `pycord.Client`. Otherwise you can use the `self.on` method
    and pass in a callback to register it for the specified event.
    """

    def __init__(self):
        super().__init__('asyncio')
        self.on('message', message_handler)

    async def on_message(self, msg):
        print("We've received a message in #{} with content \"{}\"".format(msg.channel.name, msg.content))
        await self.process_commands(msg)

    async def on_ready(self, _bootup):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        print("We're ready!")


if __name__ == '__main__':
    client = MyBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.login('token'))
