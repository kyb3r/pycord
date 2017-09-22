<div align="center">
        <p> <img src="https://i.imgur.com/SbFk45Y.png"/> </p>
        <p><i><b>A discord api wrapper in progress :)</b></i></p>
	<p> 
		<a href="https://discord.gg/pmQSbAd"><img src="https://discordapp.com/api/guilds/345787308282478592/embed.png" alt="" /></a>
		<img src="https://img.shields.io/badge/python-3.6-brightgreen.svg" alt="python 3.6" /></a>
	</p>
</div> 

## About
pycord is a discord api wrapper currently in development. Its easy to use, asynchronous and object oriented. It has a commands framework currently under development that makes it easy to write discord bots.

## Installation
You can easily install the pre-release of this library by doing `pip3 install py-cord`

## Examples

```py
import pycord

client = pycord.Client()

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

client.login('token')
```

### Commands examples

```py
import pycord

client = pycord.Client()

@client.on('ready')
async def ready():
   print('Bot online!')

@client.command()
async def ping(ctx): # the message that called the command
    await ctx.send('Pong!') # yes, it does look like d.py :/ 
			    # going for a clean style for commands anyways

@client.command() 
async def add(ctx, *numbers: int):
    await ctx.send(sum(numbers))

client.login('token')
```

How to send messages
```py
await ctx.send('content')
await channel.send('content')
await message.reply('content')
await message.channel.send('content')
```

How to send embeds
```py
em = pycord.Embed(title='Hi there', color=0x00FFFF)
em.set_author('Bob')
em.add_field('oi','this is a value')

await channel.send('pretext', embed=em)
```

We will be replacing `message` with seperate context class later on.
