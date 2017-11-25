<div align="center">
        <p> <img src="https://i.imgur.com/tDy4yb4.png"/> </p>
        <p><i><b>A Discord API wrapper in progress :)</b></i></p>
	<p> 
		<a href="https://discord.gg/Q8kuctn"><img src="https://discordapp.com/api/guilds/363717307660369921/embed.png" alt="" /></a>
		<img src="https://img.shields.io/badge/python-3.6-brightgreen.svg" alt="python 3.6" />
		<img src="https://readthedocs.org/projects/pycord/badge/?version=dev" alt="docs" /></a>
	</p>
</div> 

## About
Pycord is a Discord API wrapper currently in development. It's easy to use, object oriented and asynchronous, using multio to support both trio and curio async libraries. It features a super simple commands framework inspired by discord.py's one that makes writing Discord bots a breeze.

## Installation
You can easily install the pre-release of this library by doing `pip3 install py-cord` (not the latest)

## Examples

```py
import pycord

client = pycord.Client()

@client.on('ready')
async def on_ready(time):
    print(f'Booted up in {time:.2f} seconds')
    print(f'Logged in as: {client.user}')
    print(f'User ID: {client.user.id}')
    print(f'Is Bot: {client.user.bot}')
    print(f'With {len(client.guilds)} guilds')

@client.on('message')
async def ping_command(message):
    if message.content.startswith('py.ping'):
        await message.reply('Pong!')

message_count = 0

@client.on('message')
async def stats(message):
    message_count += 1
 
# easily register multiple events

client.login('token')
```

### Commands examples

How to send messages
```py
await ctx.reply('content')
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

