from discord.ext import commands
import discord
import asyncio


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel_id = payload.channel_id
        channel = self.client.get_channel(channel_id)
        if payload.emoji.id == 399692392594407436:
            await channel.send('https://tenor.com/view/el-huevo-gif-18925090')
            print(payload.member.nick)

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

    @commands.command(name='mega', hidden=True)
    async def mega(self, context):
        if context.author.id != 398633288077410305:
            await context.send('This command is restricted to Varcexion')
            return
        await context.send('https://cdn.discordapp.com/attachments/783474197526609930/799297338191511552/unknown.png')

    @commands.command(name='zer0', hidden=True)
    async def zer0(self, context):
        if context.author.id != 363554630296272896 and context.author.id != 288079528914452480 and context.author.id \
                != 326817025638924289 and context.author.id != 634649274533150720:
            await context.send(f'This command is restricted to Zer0')
            return
        await context.send('https://cdn.discordapp.com/attachments/746767192116166706/799478175460753430/Idle_Ze'
                           'r0_Darkness.gif')

    @commands.command(name='neko', hidden=True)
    async def neko(self, context):
        if context.author.id != 449622694682689547 and context.author.id != 609870075037483008:
            await context.send(f"This is lock's private command.")
            return
        await context.send('this is weird, hence there no longer being an image of it')

    @commands.command(name='bounce', hidden=True)
    async def bounce(self, context):
        await context.send('https://cdn.discordapp.com/attachments/434427391729729552/803716155947614250/Wtf.gif')


def setup(client):
    client.add_cog(fun(client))
