import pycord
import trio

"""
Example showing off how beautiful 
the design of this api wrapper is ;)
"""

client = pycord.Client('trio')


@client.on('ready')
async def on_ready(time):
    print(f'Logged in as: {client.user}')
    print(f'User ID: {client.user.id}')
    print(f'Is Bot: {client.user.bot}')
    print(f'With {len(client.guilds)} guilds')


@client.on('message')
async def ping_command(message):
    if message.content.startswith('py.ping'):
        await message.reply('Pong!')


trio.run(client.login, 'token')
