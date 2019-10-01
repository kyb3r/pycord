import pycord
import trio

client = pycord.Client('trio', prefixes='a.')


@client.on('ready')
async def ready(time):
    print('ready')


@client.on('message')
async def on_message(msg):
    await client.process_commands(msg)


def is_owner(ctx):
    return ctx.author.id == 122739797646245899


@client.cmd('ping')
async def ping(ctx) -> is_owner:
    await ctx.reply('Pong!')


trio.run(client.login, 'token')
