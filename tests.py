from pycord import Client
import asyncio

client = Client()

class Channel: #placeholder
    def __init__(self, id):
        self.id = id

@client.on('ready')
async def ready_event():
    print(f'Logged in as: {client.user.username}')
    print(f'User ID: {client.user.id}')
    print(f'Is Bot: {client.user.bot}')

    for guild in client.guilds:
        print(guild.id, guild.unavailable)

@client.on('message')
async def command_test(data):
    channel = Channel(int(data['channel_id']))
    if data['content'].startswith('py.ping'):
        await client.api.send_message(channel, content='pong!')

client.login('token')

# from pycord.models.user import ClientUser

# user = {
#     "avatar":"fb405db5b7847c5f113ece6e33e0d51f",
#     "bot":True,
#     "discriminator":"5599",
#     "email": None,
#     "id":"354218232426528768",
#     "mfa_enabled": True,
#     "username":"API-Tests",
#     "verified": True
# }

# test = ClientUser(user)

# print(test.username)