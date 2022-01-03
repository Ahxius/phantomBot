from discord.ext import commands
from discord import Embed
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()


class ProbationaryPortal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("execute")
    @commands.is_owner()
    async def update(self, context, content):
        try:
            response = c.execute(content)
            conn.commit()
        except sqlite3.Error:
            await context.send("Error whilst attempting to execute command.")
            return
        await context.send(response.fetchall())

    @commands.Cog.listener()
    async def on_message(self, message):
        logsChannel = self.client.get_guild(364962599508508672).get_channel(917134252875870270)
        if message.channel.id != logsChannel.id or len(message.embeds) == 0:
            return
        embed = message.embeds[0]
        username = embed.author.name
        rawTime = None
        for field in embed.fields:
            if field.name == "__Recorded Time:__":
                rawTime = field.value
        time = (int(rawTime[:2]) * 3600) + (int(rawTime[3:5]) * 60) + int(rawTime[6:8])
        try:
            totalSeconds = c.execute(f'SELECT secondsPatrolled FROM probieInfo '
                                     f'WHERE username = "{username}"').fetchone()[0]
            totalSeconds += time
            c.execute(f"UPDATE probieInfo SET secondsPatrolled = {totalSeconds} WHERE username = '{username}'")
        except TypeError:
            c.execute(f"INSERT INTO probieInfo (username, eventsAttended, secondsPatrolled, merits, demerits) "
                      f"VALUES ('{username}', 0, {time}, 0, 0) ")
        conn.commit()

    @commands.command("addevent")
    async def addevent(self, context):
        if self.client.get_guild(364962599508508672).get_role(697605737999761408) not in context.author.roles and \
                self.client.get_guild(364962599508508672).get_role(797923064004083732) not in context.author.roles:
            await context.send(f'This command requires either the ``VEIL`` or ``TRIAL EVALUATOR`` role to be used.')
            return
        if len(context.message.content) == 10:
            await context.send(f'{context.author.mention}, please include a list of attendees separated by a space.')
            return
        logChannel = self.client.get_guild(364962599508508672).get_channel(676604257905934399)
        users = context.message.content[11:].split(" ")
        for user in users:
            try:
                eventsAttended = c.execute(f'SELECT eventsAttended FROM probieInfo'
                                           f' WHERE username = "{user}"').fetchone()[0]
                eventsAttended += 1
                c.execute(f"UPDATE probieInfo SET eventsAttended = {eventsAttended} WHERE username = '{user}'")
            except TypeError:
                c.execute(f"INSERT INTO probieInfo (username, eventsAttended, secondsPatrolled, merits, demerits) "
                          f"VALUES ('{user}', 1, 0, 0, 0) ")
        conn.commit()
        embed = Embed(title="Trial Event Added", color=0x000000, description=f"**Host:** {context.author.mention}\n"
                                                                             f"**Attendees:** {', '.join(users)}")
        await logChannel.send(embed=embed)

    @commands.command("merit")
    async def merit(self, context, user, *reason):
        if self.client.get_guild(364962599508508672).get_role(697605737999761408) not in context.author.roles and \
                self.client.get_guild(364962599508508672).get_role(797923064004083732) not in context.author.roles:
            await context.send(f'This command requires either the ``VEIL`` or ``TRIAL EVALUATOR`` role to be used.')
            return
        if len(context.message.content) == 7:
            await context.send(f"{context.author.mention}, please include both the user's Roblox username and reason.")
        logChannel = self.client.get_guild(364962599508508672).get_channel(676604257905934399)
        try:
            merits = c.execute(f'SELECT merits FROM probieInfo WHERE username = "{user}"').fetchone()[0]
            merits += 1
            c.execute(f"UPDATE probieInfo SET merits = {merits} WHERE username = '{user}'")
        except TypeError:
            c.execute(f"INSERT INTO probieInfo (username, eventsAttended, secondsPatrolled, merits, demerits) "
                      f"VALUES ('{user}', 0, 0, 1, 0) ")
        conn.commit()
        embed = Embed(title="Trial Merit Given", color=0x000000, description=f"**Evaluator:** {context.author.mention}"
                                                                             f"\n"
                                                                             f"**Recipient:** {user}\n"
                                                                             f"**Reason:** {' '.join(reason)}")
        await logChannel.send(embed=embed)

    @commands.command("demerit")
    async def demerit(self, context, user, *reason):
        if self.client.get_guild(364962599508508672).get_role(697605737999761408) not in context.author.roles and \
                self.client.get_guild(364962599508508672).get_role(797923064004083732) not in context.author.roles:
            await context.send(f'This command requires either the ``VEIL`` or ``TRIAL EVALUATOR`` role to be used.')
            return
        if len(context.message.content) == 9:
            await context.send(
                f"{context.author.mention}, please include both the user's Roblox username and reason.")
            return
        logChannel = self.client.get_guild(364962599508508672).get_channel(676604257905934399)
        try:
            demerits = c.execute(f'SELECT demerits FROM probieInfo WHERE username = "{user}"').fetchone()[0]
            demerits += 1
            c.execute(f"UPDATE probieInfo SET demerits = {demerits} WHERE username = '{user}'")
        except TypeError:
            c.execute(f"INSERT INTO probieInfo (username, eventsAttended, secondsPatrolled, merits, demerits) "
                      f"VALUES ('{user}', 0, 0, 0, 1) ")
        conn.commit()
        embed = Embed(title="Trial Demerit Given", color=0x000000,
                      description=f"**Evaluator:** {context.author.mention}\n"
                                  f"**Recipient:** {user}\n"
                                  f"**Reason:** {' '.join(reason)}")
        await logChannel.send(embed=embed)

    @commands.command("trialinfo")
    async def trialinfo(self, context, username: str = None):
        if not username:
            await context.send(f'{context.author.mention}, please include Roblox username.')
            return
        try:
            response = c.execute(f'SELECT * FROM probieInfo WHERE username = "{username}"').fetchone()
            seconds = response[2] % (24 * 3600)
            hours = seconds // 3600
            seconds %= 3600
            minutes = response[2] // 60
            seconds %= 60
            hours = str(int(hours))
            minutes = str(int(minutes))
            seconds = str(int(seconds))
            if len(hours) == 1:
                hours = "0" + hours
            if len(minutes) == 1:
                minutes = "0" + minutes
            if len(seconds) == 1:
                seconds = "0" + seconds
            totalTime = hours + ":" + minutes + ":" + seconds
            embed = Embed(title=f"{response[0]}'s Trial Information", color=0x000000,
                          description=f"**Events Attended:** {response[1]}\n**Patrol Time:** {totalTime}\n"
                                      f"**Merits:** {response[3]}\n**Demerits:** {response[4]}")
            await context.send(embed=embed)
        except TypeError:
            await context.send("There is no information stored for this user. If you believe this is an error,"
                               " please DM <@!193051160616239104>.")

    @commands.command("top")
    async def top(self, context):
        message = await context.send(embed=Embed(title="Select an option:", description=":one: - Event Attendance\n"
                                                                                        ":two: - Patrol Time\n"
                                                                                        ":three: - Merits\n"
                                                                                        ":four: - Demerits"))
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        await message.add_reaction("4️⃣")

        def check(reaction_checking, user_checking):
            return user_checking == context.author

        reaction, user = await self.client.wait_for('reaction_add', check=check)
        await message.delete()
        if reaction.emoji == "1️⃣":
            page = 1
            count = 10
            start = 0
            continueLoop = True
            while continueLoop:
                try:
                    responses = c.execute(
                        f"SELECT username, eventsAttended from probieInfo ORDER BY eventsAttended "
                        f"DESC LIMIT 10 OFFSET {start}").fetchall()
                    if len(responses) == 0:
                        await context.send("Reached end of database.")
                        return
                    description = ""
                    for response in responses:
                        description += f"**{response[0]}**: {response[1]}\n"
                    embed = Embed(title=f"Events Attended Leaderboard - Page {page}", description=description)
                    lbMessage = await context.send(embed=embed)
                    await lbMessage.add_reaction("\U000025c0")
                    await lbMessage.add_reaction("\U000025b6")
                    await lbMessage.add_reaction("\U0000274c")
                    reaction, user = await self.client.wait_for("reaction_add", check=check)
                    await lbMessage.delete()
                    if reaction.emoji == "\U000025c0":  # backward
                        if start == 0:
                            await context.send("You are at the first page. Idiot.")
                            continueLoop = False
                        else:
                            start -= count
                            page -= 1
                    elif reaction.emoji == "\U000025b6":  # forward
                        start += count
                        page += 1
                    elif reaction.emoji == "\U0000274c":  # exit
                        continueLoop = False
                except sqlite3.Error:
                    await context.send("Error occurred retrieving from database. Contact Ahxius.")
                    return
            return
        elif reaction.emoji == "2️⃣":
            page = 1
            count = 10
            start = 0
            continueLoop = True
            while continueLoop:
                try:
                    responses = c.execute(
                        f"SELECT username, secondsPatrolled from probieInfo ORDER BY secondsPatrolled "
                        f"DESC LIMIT 10 OFFSET {start}").fetchall()
                    if len(responses) == 0:
                        await context.send("Reached end of database.")
                        return
                    description = ""
                    for response in responses:
                        seconds = response[1] % (24 * 3600)
                        hours = seconds // 3600
                        seconds %= 3600
                        minutes = response[1] // 60
                        seconds %= 60
                        hours = str(int(hours))
                        minutes = str(int(minutes))
                        seconds = str(int(seconds))
                        if len(hours) == 1:
                            hours = "0" + hours
                        if len(minutes) == 1:
                            minutes = "0" + minutes
                        if len(seconds) == 1:
                            seconds = "0" + seconds
                        description += f"**{response[0]}**: {hours}:{minutes}:{seconds}\n"
                    embed = Embed(title=f"Patrol Time Leaderboard - Page {page}", description=description)
                    lbMessage = await context.send(embed=embed)
                    await lbMessage.add_reaction("\U000025c0")
                    await lbMessage.add_reaction("\U000025b6")
                    await lbMessage.add_reaction("\U0000274c")
                    reaction, user = await self.client.wait_for("reaction_add", check=check)
                    await lbMessage.delete()
                    if reaction.emoji == "\U000025c0":  # backward
                        if start == 0:
                            await context.send("You are at the first page. Idiot.")
                            continueLoop = False
                        else:
                            start -= count
                            page -= 1
                    elif reaction.emoji == "\U000025b6":  # forward
                        start += count
                        page += 1
                    elif reaction.emoji == "\U0000274c":  # exit
                        continueLoop = False
                except sqlite3.Error:
                    await context.send("Error occurred retrieving from database. Contact Ahxius.")
                    return
            return
        elif reaction.emoji == "3️⃣":
            page = 1
            count = 10
            start = 0
            continueLoop = True
            while continueLoop:
                try:
                    responses = c.execute(
                        f"SELECT username, merits from probieInfo ORDER BY merits "
                        f"DESC LIMIT 10 OFFSET {start}").fetchall()
                    if len(responses) == 0:
                        await context.send("Reached end of database.")
                        return
                    description = ""
                    for response in responses:
                        description += f"**{response[0]}**: {response[1]}\n"
                    embed = Embed(title=f"Merits Received Leaderboard - Page {page}", description=description)
                    lbMessage = await context.send(embed=embed)
                    await lbMessage.add_reaction("\U000025c0")
                    await lbMessage.add_reaction("\U000025b6")
                    await lbMessage.add_reaction("\U0000274c")
                    reaction, user = await self.client.wait_for("reaction_add", check=check)
                    await lbMessage.delete()
                    if reaction.emoji == "\U000025c0":  # backward
                        if start == 0:
                            await context.send("You are at the first page. Idiot.")
                            continueLoop = False
                        else:
                            start -= count
                            page -= 1
                    elif reaction.emoji == "\U000025b6":  # forward
                        start += count
                        page += 1
                    elif reaction.emoji == "\U0000274c":  # exit
                        continueLoop = False
                except sqlite3.Error:
                    await context.send("Error occurred retrieving from database. Contact Ahxius.")
                    return
            return
        elif reaction.emoji == "4️⃣":
            page = 1
            count = 10
            start = 0
            continueLoop = True
            while continueLoop:
                try:
                    responses = c.execute(
                        f"SELECT username, demerits from probieInfo ORDER BY demerits "
                        f"DESC LIMIT 10 OFFSET {start}").fetchall()
                    if len(responses) == 0:
                        await context.send("Reached end of database.")
                        return
                    description = ""
                    for response in responses:
                        description += f"**{response[0]}**: {response[1]}\n"
                    embed = Embed(title=f"Demerits Received Leaderboard - Page {page}", description=description)
                    lbMessage = await context.send(embed=embed)
                    await lbMessage.add_reaction("\U000025c0")
                    await lbMessage.add_reaction("\U000025b6")
                    await lbMessage.add_reaction("\U0000274c")
                    reaction, user = await self.client.wait_for("reaction_add", check=check)
                    await lbMessage.delete()
                    if reaction.emoji == "\U000025c0":  # backward
                        if start == 0:
                            await context.send("You are at the first page. Idiot.")
                            continueLoop = False
                        else:
                            start -= count
                            page -= 1
                    elif reaction.emoji == "\U000025b6":  # forward
                        start += count
                        page += 1
                    elif reaction.emoji == "\U0000274c":  # exit
                        continueLoop = False
                except sqlite3.Error:
                    await context.send("Error occurred retrieving from database. Contact Ahxius.")
                    return
            return
        else:
            await context.send("You added a different reaction! Nice try:)")
            return

    @commands.command("remove")
    async def remove(self, context, user: str = None):
        if self.client.get_guild(364962599508508672).get_role(697605737999761408) not in context.author.roles or \
                len(user) == 0:
            await context.send(f"{context.author.mention}, make sure you have the VEIL role and are providing a user.")
            return
        try:
            c.execute(f"DELETE FROM probieInfo WHERE username = '{user}'")
            await context.send(f"``{user}`` successfully removed from database.")
            await self.client.get_guild(364962599508508672).get_channel(676604257905934399)\
                .send(f'{user} removed from database by {context.author.mention}.')
        except sqlite3.Error:
            await context.send("There was an error. Please try again.")


def setup(client):
    client.add_cog(ProbationaryPortal(client))
