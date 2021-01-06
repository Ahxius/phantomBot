import os
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

discord_client = Bot(command_prefix='p?')


@discord_client.event
async def on_ready():
    print(f'Discord login successful - {discord_client.user}')


@discord_client.event
async def on_raw_reaction_add(payload):
    channel_id = payload.channel_id
    channel = discord_client.get_channel(channel_id)
    if payload.emoji.id == 399692392594407436:
        await channel.send('https://tenor.com/view/el-huevo-gif-18925090')
        print(payload.member.nick)


@discord_client.command(name='wizardlizard', hidden=True)
async def wizardlizard(context):
    member_roles = context.author.roles
    phantom_server = discord_client.get_guild(364962599508508672)
    lizard_object = phantom_server.get_role(760904501598617601)
    if lizard_object not in member_roles:
        await context.send('nice try nerd')
        return
    await context.send('https://tenor.com/view/lizard-snowing-mage-staff-gif-10597733')


@discord_client.command(name='send', aliases=['s'])
async def send(context, *, content: str = 0):
    member_roles = context.author.roles
    phantom_server = discord_client.get_guild(364962599508508672)  # should = phantom guild id
    role_object = phantom_server.get_role(796203797714042910)
    if context.author.id != 193051160616239104 and role_object not in member_roles:
        await context.send(f"This command requires the ``SHROUD`` role for it to be used.")
        return
    if content == 0:
        await context.send(f'{context.author.mention} Command syntax: ``p?send <message>``')
        return
    message = context.message
    await message.delete()
    await context.send(content)


discord_client.run(TOKEN)
