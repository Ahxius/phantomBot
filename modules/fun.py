from discord.ext import commands, tasks
import datetime
import discord
import asyncio
import sqlite3
import random
import string

conn = sqlite3.connect('database.db')
c = conn.cursor()


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.reference is not None:
            if message.reference.cached_message.content == "sometimes i dream about cheese":
                for user_password in c.execute("SELECT password FROM elHuevo").fetchall():
                    if user_password[0] == message.content:
                        await message.channel.send('https://tenor.com/view/el-huevo-gif-18925090')
                        await message.delete()

    @tasks.loop(hours=24)
    async def daily_task(self):
        user_ids = c.execute("SELECT user_id FROM elHuevo").fetchall
        for user_id in user_ids:
            password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            c.execute(f"UPDATE elHuevo SET password = {password}) WHERE user_id = {user_id}")
            await self.client.get_user(user_id).send(f"Your El Huevo password has been changed to: ``{password}``")

    @daily_task.before_loop
    async def wait_until_midnight(self):
        now = datetime.datetime.now().astimezone()
        next_run = now.replace(hour=0, minute=0, second=0)
        if next_run < now:
            next_run += datetime.timedelta(days=1)
        await discord.utils.sleep_until(next_run)

    @commands.command(name="resetpassword", hidden=True)
    @commands.is_owner()
    async def resetpassword(self, context):
        user_ids = c.execute("SELECT user_id FROM elHuevo").fetchall()
        for user_id in user_ids:
            print
            user_password = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            c.execute(f"UPDATE elHuevo SET password = '{user_password}' WHERE user_id = {user_id[0]}")
            conn.commit()
            user = await self.client.fetch_user(user_id[0])
            await user.send(f"Your El Huevo password has been changed to: ``{user_password}``")
        await context.send("Completed, master.")

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
        await context.author.edit(reason="ROMANIAN ALERT", nick=f'ROMANIAN')


def setup(client):
    client.add_cog(Fun(client))
