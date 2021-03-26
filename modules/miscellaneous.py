from discord.ext import commands
import asyncio
import sys
import os
from dotenv import load_dotenv
import requests

load_dotenv()
git_pass = os.getenv('GITHUB_PASSWORD')
paste_token = os.getenv('PASTE_TOKEN')


class miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='send', aliases=['s'], help='Sends message as PHANTOM bot')
    async def send(self, context, *, content: str = 0):
        member_roles = context.author.roles
        phantom_server = self.client.get_guild(364962599508508672)  # should = phantom guild id
        role_object = phantom_server.get_role(761957228151832587)
        if context.author.id != 193051160616239104 and role_object not in member_roles:
            await context.send(f"This command requires the ``SHROUD`` role for it to be used.")
            return
        if content == 0:
            await context.send(f'{context.author.mention} Command syntax: ``p?send <message>``')
            return
        message = context.message
        await message.delete()
        await context.send(content)

    @commands.command(name='shutdown', aliases=['sd'], hidden=True)
    @commands.is_owner()
    async def shutdown(self, context):
        await context.send('Shutting down...')
        sys.exit()

    @commands.command(name='update', hidden=True)
    @commands.is_owner()
    async def update(self, context):
        clone_exit = os.system(f'git clone https://Ahxius:{git_pass}@github.com/Ahxius/phantomBot.git '
                               f'~/phantomBot-temp')
        if clone_exit == 0:
            await context.send('Clone successful, copying files into main directory.')
            copy_exit = os.system('cd ~/phantomBot-temp && cp ~/phantomBot-temp/*.py ~/phantomBot && cp '
                                  '~/phantomBot-temp/modules/*.py ~/phantomBot/modules')
            if copy_exit == 0:
                await context.send('Copy successful, reloading extensions.')
                os.system('sudo rm ~/phantomBot-temp -r')
                for cog in os.listdir('modules'):
                    if not cog.endswith('.py'):
                        continue
                    try:
                        self.client.unload_extension(f'modules.{cog[:-3]}')
                        self.client.load_extension(f'modules.{cog[:-3]}')
                    except Exception as e:
                        await context.send(e)
                await context.send('Bot successfully updated from GitHub')

    @commands.command(name='dpaste', aliases=['text', 'txt'])
    async def dpaste(self, context, expiry=None, language=None):
        if not expiry:
            await context.send("``p?txt <ttl (days)> <filetype (opt)>``")
            return
        await context.send(f"{context.author.mention}, please send your text.")

        def check(m):
            return m.author == context.author and m.channel == context.channel
        content = await self.client.wait_for('message', check=check)
        payload = {"content": content.content, "expiry_days": int(expiry), "syntax": language}
        request = requests.post("https://dpaste.com/api/", data=payload)
        await content.delete()
        await context.send(f"Here's your link: {request.text}")

    @commands.command(name='channel', aliases=['private', 'vc', 'temp'])
    async def channel(self, context, quantity: int = None):

        if not quantity:
            await context.send("``p?channel <max amt of people>``")
            return
        phantom_server = self.client.get_guild(364962599508508672)
        for category in phantom_server.categories:
            if category.id == 824845560992759849:
                private_category = category
                break
        x = 1
        for channel in phantom_server.voice_channels:
            if 'Private VC' in channel.name:
                x += 1
        # noinspection PyUnboundLocalVariable
        voice_channel = await phantom_server.create_voice_channel(name=f'Private VC #{x}', user_limit=quantity,
                                                                  reason=f'Requested by {context.author.nick}',
                                                                  category=private_category)
        await asyncio.sleep(30)
        if not voice_channel.members:
            await context.send(f'{context.author.mention}, your private VC timed out.')
            await voice_channel.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if 'Private VC' in before.channel.name and not before.channel.members:
            await before.channel.delete()

    @commands.command(name='clean')
    async def clean(self, context):
        member_roles = context.author.roles
        phantom_server = self.client.get_guild(364962599508508672)
        shroud_role = phantom_server.get_role(761957228151832587)
        if shroud_role not in member_roles and context.author.id != 193051160616239104:
            await context.send(f'You do not have proper permissions to use this command.')
            return
        voice_channels = phantom_server.voice_channels
        for channel in voice_channels:
            if 'Private VC' in channel.name:
                await channel.delete()


def setup(client):
    client.add_cog(miscellaneous(client))
