import pycord
import curio

"""
Example showing off how beautiful 
the design of this api wrapper is ;)
"""

client = pycord.Client('curio')


@client.on('ready')
async def on_ready():
    print(f'Logged in as: {client.user}')
    print(f'User ID: {client.user.id}')
    print(f'Is Bot: {client.user.bot}')
    print(f'With {len(client.guilds)} guilds')


@client.on('message')
async def ping_command(message):
    if message.content.startswith('py.ping'):
        await message.reply('Pong!')


curio.run(client.login, 'NTg5OTMxNDIwNTA0MjkzMzk5.XZId5Q.zXTcXoZwYZVxPYo8LlVoOw83R2U')
