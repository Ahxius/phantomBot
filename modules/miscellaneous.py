from discord.ext import commands
import asyncio
import sys
import random


class miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='send', aliases=['s'], help='Sends message as PHANTOM bot')
    async def send(self, context, *, content: str = 0):
        member_roles = context.author.roles
        phantom_server = self.client.get_guild(364962599508508672)  # should = phantom guild id
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


def setup(client):
    client.add_cog(miscellaneous(client))
