import pycord

client = pycord.Client()

@client.on('ready')
async def on_ready():
    print(f'Logged in as: {client.user}')
    print(f'User ID: {client.user.id}')
    print(f'Is Bot: {client.user.bot}')
    print(f'With {len(client.guilds)} guilds')

@client.on('message')
async def on_message(message):
    if message.content.startswith('py.ping'):
        await message.reply('Pong!')

client.login('token')
