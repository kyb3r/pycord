"""
MIT License

Copyright (c) 2017 verixx / king1600

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime

import pycord
import trio


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
        super().__init__('trio')
        self.on('message', self.message_handler)

    async def on_message(self, msg):
        print("We've received a message in #{} with content \"{}\"".format(msg.channel.name, msg.content))
        await self.process_commands(msg)

    async def on_ready(self, _bootup):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        print("We're ready!")


if __name__ == '__main__':
    client = MyBot()
    trio.run(client.login, 'NTg5OTMxNDIwNTA0MjkzMzk5.XZFIQw.3FmrlCRKjbB0yUrh-xXVYLYYz8U')
