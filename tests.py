import pycord
import traceback
import time

client = pycord.Client()

@client.on('ready')
async def on_ready():
    bootup = time.time() - client._boot_up_time
    print('--------------------')
    print(f'Bootup time: {bootup:.2f} secs')
    print(f'Logged in as: {client.user}')
    print(f'With {len(client.guilds)} guilds')
    print(f'And {len(client.users)} users') # gotta do some chunking
    print(f'User ID: {client.user.id}')
    print(f'Is Bot: {client.is_bot}')
    print('--------------------')

@client.on('message')
async def on_message(message):
    if message.content.startswith('py.ping'):
        await message.reply('Pong!')
    if message.content.startswith('py.guildinfo'):
        await message.reply(str(message.guild))

@client.on('error')
async def error_handler(e):
    traceback.print_exc()
    

client.login("token")
