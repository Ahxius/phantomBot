from discord.ext import commands
import asyncio
import sys
import random
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

    @commands.command(name='giveaway', aliases=['g'], help='Begins a giveaway', hidden=True)
    async def giveaway(self, context, hours=None, *, prize=None):
        if hours and prize is None or hours or prize is None:
            await context.send(f'{context.author.mention} Command syntax: ``p?giveaway <time in hours> <prize>``')
            return
        channel = self.client.get_channel(722141971736559695)  # change
        message = await channel.send(f"{context.author.mention} is giving away {prize}! Giveaway will end in {hours}"
                                     f" hours.")
        await message.add_reaction('\U0001f389')
        time = float(hours) * 60 * 60
        await asyncio.sleep(time)
        message = await channel.fetch_message(message.id)
        user = await message.reactions[0].users().flatten()
        winner = random.choice(user)
        while winner.id == 717445341217030238:
            winner = random.choice(user)
        await channel.send(f'{winner.mention} has won the giveaway! DM {context.author.mention} to claim.')

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

    # @commands.command(name='channel', aliases=['private', 'vc', 'temp'])
    # async def channel(self, context, quantity: int = None):
    #     if not quantity:
    #         await context.send("``p?channel <max amt of people>``")
    #         return
    #     phantom_server = await self.client.get_guild(364962599508508672)
    #     categories = await phantom_server.categories
    #     for category in categories:
    #         if category.id == ''
    #     await phantom_server.create_voice_channel(name='Private VC', user_limit=quantity,
    #                                               reason=f'Requested by {context.author.nick}', category=)

    @commands.command(name='create')
    async def create(self, context):
        phantom_server = await self.client.get_guild(364962599508508672)
        await phantom_server.create_category(name='- - { PHANTOM PRIVATE } - -', position=5)



def setup(client):
    client.add_cog(miscellaneous(client))
