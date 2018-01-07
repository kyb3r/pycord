import pycord
import trio
import datetime

client = pycord.Client(prefixes='py.')


@client.on('ready')
async def on_ready(bootup):
    print('--------------------')
    print('Internal Cache Ready.')
    print(f'Bootup time: {bootup:.2f} secs')
    print(f'Logged in as: {client.user}')
    print(f'With {len(client.guilds)} guilds')
    print(f'And {len(client.users)} users') # gotta do some chunking
    print(f'User ID: {client.user.id}')
    print(f'Is Bot: {client.is_bot}')
    print('--------------------')




def dynamic_properties(generic):
    def wrapper(cls):
        for name in generic:
            def getter(self, x=name):
                return self.db.get_value(self.id, name)

            def setter(self, value, x=name):
                return self.db.set_value(self.id, name, value)

            prop = property(getter, setter)
            setattr(cls, name, property)
        return cls
    return wrapper

generic_properties = ['join_message', 'leave_message', 'etc..']
@dynamic_properties()
class ConfigThingo:
    ...              

async def on_message(message):
    if message.content.startswith('py.ping'):
        await message.reply('Pong!')


@client.cmd('ping')
async def ping(ctx):
    await ctx.reply('Pong!')


@client.on('member_join')
async def on_member_join(member):
    channel = member.guild.channels.get(456789) # channel id
    await channel.send(f'Welcome to **{member.guild}** {member.mention}!')

@client.cmd('guildinfo', aliases=['serverinfo', 'si'])
async def serverinfo(ctx):
    guild = ctx.guild
    days = (datetime.datetime.utcnow() - guild.created_at).days
    online = sum(1 for m in guild.members if m.status != 'offline')

    em = pycord.Embed(color=0x00FFFF)
    em.timestamp = guild.created_at
    em.add_field('Name', guild)
    em.add_field('Owner', guild.owner)
    em.add_field('Roles', len(guild.roles))
    em.add_field('Channels', len(guild.channels))
    em.add_field('Region', guild.region)
    em.add_field('Members', f'{online}/{len(guild.members)}')
    em.add_field('ID', guild.id)
    em.set_thumbnail(guild.icon_url)
    em.set_footer(f'Created {days} day(s) ago')

    await ctx.reply(f'Here you go {ctx.author.mention}!', embed=em)

def owner(ctx): # command check
    return ctx.author.id == 325012556940836864

@pycord.cmd('say') # raw command decorator
async def echo(ctx, *, message) -> owner: 
    await ctx.reply(message)

client.commands.add(echo) # manually adding commands

@client.cmd('eval')
async def pyeval(ctx, *, code) -> owner:
    # do stuff to evaluate python code
    await ctx.reply(f'```py\n{code}\n```')

client.login("token")
