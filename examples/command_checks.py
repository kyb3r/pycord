import pycord 
import multio

client = pycord.Client()

@client.on('ready')
async def ready(time):
    print('ready')

def is_owner(ctx):
    return ctx.author.id == 319395783847837696

@client.cmd('ping')
async def ping(ctx) -> is_owner:
    await ctx.send('Pong!')

client.login("token")