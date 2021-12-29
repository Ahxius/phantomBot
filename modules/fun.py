from discord.ext import commands
import discord
import asyncio
import sqlite3

conn = sqlite3.connect('ahxius')
c = conn.cursor()


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        channel = self.client.get_channel(channel_id)
        if payload.emoji.id == 399692392594407436:
            await channel.send('https://tenor.com/view/el-huevo-gif-18925090')

    @commands.command(name='wizardlizard', hidden=True, help='Become a wizard lizard today!')
    async def wizardlizard(self, context):
        member_roles = context.author.roles
        phantom_server = self.client.get_guild(364962599508508672)
        lizard_object = phantom_server.get_role(760904501598617601)
        if lizard_object not in member_roles:
            await context.send('nice try nerd')
            return
        await context.send('https://tenor.com/view/lizard-snowing-mage-staff-gif-10597733')

    @commands.command(name='banana', hidden=True)
    async def banana(self, context):
        banana_embed = discord.Embed(title='Banana', color=0xFFFF00)
        channel = context.channel
        message = await channel.send(embed=banana_embed)
        boom_embed = discord.Embed(title='BOOM', color=0xFF0000)
        await asyncio.sleep(3)
        await message.edit(embed=boom_embed)

    @commands.command(name='neko', hidden=True)
    async def neko(self, context):
        if context.author.id != 449622694682689547 and context.author.id != 609870075037483008:
            await context.send(f"This is lock's private command.")
            return
        await context.send("hii lock i don't remember the gif that you wanted me to change this to")

    @commands.command(name='bounce', hidden=True)
    async def bounce(self, context):
        await context.send('https://cdn.discordapp.com/attachments/434427391729729552/803716155947614250/Wtf.gif')

    @commands.command(name="godmode", hidden=True)
    async def godmode(self, context):
        await context.author.edit(reason="ROMANIAN ALERT", nick=f'[ROMANIAN] {context.author.nick}')


def setup(client):
    client.add_cog(Fun(client))
