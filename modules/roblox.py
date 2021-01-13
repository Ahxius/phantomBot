from discord.ext import commands
import robloxapi
from robloxapi.utils import errors
import os
from dotenv import load_dotenv

load_dotenv()
COOKIE = os.getenv('ROBLOX_COOKIE')

roblox_client = robloxapi.Client(COOKIE)


class roblox(commands.Cog):
    def __init__(self, discord_client):
        self.discord_client = discord_client

    @commands.Cog.listener()
    async def on_ready(self):
        self_object = await roblox_client.get_self()
        print(f'Roblox login successful - {self_object.name}')

    @commands.command(name='exile', aliases=['e'], help='Exiles given user')
    async def exile(self, context, member: str = 0):
        member_roles = context.author.roles
        phantom_server = self.discord_client.get_guild(364962599508508672)  # should = phantom guild id
        role_object = phantom_server.get_role(761957228151832587)  # should = shroud id
        trial_object = phantom_server.get_role(607971962873970690)  # should = trial overseer id
        if trial_object not in member_roles and role_object not in member_roles:
            await context.send(f'This command requires either the ``SHROUD`` or ``Trial Overseer`` role to be used.')
            return
        if member == 0:
            await context.send(f'{context.author.mention} Command syntax: `p?exile <member>`')
            return
        user_object = await roblox_client.get_user_by_username(member)
        phantom_group = await roblox_client.get_group(3248486)
        user_id = user_object.id
        while True:
            try:
                await phantom_group.exile(user_id)
                await context.send(f'{member} has been exiled by {context.author.mention}.')
                break
            except robloxapi.utils.errors.BadStatus:
                await context.send(
                    f"Error; either I couldn't find user {member}, or I don't have high enough permissions "
                    f"to exile them.")
                break

    @commands.command(name='approve', aliases=['app'], help="Approves given user's join request")
    async def approve(self, context, member: str = 0):
        member_roles = context.author.roles
        phantom_server = self.discord_client.get_guild(364962599508508672)  # should = phantom guild id
        role_object = phantom_server.get_role(796203797714042910)  # should = shroud id
        if (role_object not in member_roles) and (context.author.id != 193051160616239104):
            await context.send(f'This command requires the ``SHROUD`` role to be used.')
            return
        if member == 0:
            await context.send(f'{context.author.mention} Command syntax: `p?approve <member>')
            return
        phantom_group = await roblox_client.get_group(3248486)
        requests = await phantom_group.get_join_requests()
        for request in requests:
            if request.user.name == member:
                await request.accept()
                await context.send(f'{member} has been accepted into the PHANTOM group.')
                return
        await context.send(f"{member} couldn't be found in the join requests.")

    @commands.command(name='promote', aliases=['p'], help='Promotes given user')
    async def promote(self, context, member: str = 0):
        member_roles = context.author.roles
        phantom_server = self.discord_client.get_guild(364962599508508672)  # should = phantom guild id
        role_object = phantom_server.get_role(697605737999761408)  # should = veil id
        if role_object not in member_roles:
            await context.send(f'This command requires the ``VEIL`` role to be used.')
            return
        if member == 0:
            await context.send(f'{context.author.mention} Command syntax: `p?promote <member>`')
            return
        phantom_group = await roblox_client.get_group(3248486)
        member_object = await roblox_client.get_user(member)
        member_id = member_object.id
        while True:
            try:
                await phantom_group.promote(member_id)
                await context.send(f"{member} has been promoted by {context.author.mention}")
                break
            except robloxapi.utils.errors.NotFound:
                await context.send(f"Error; {member} couldn't be found in the group.")
                break
            except robloxapi.utils.errors.BadStatus:
                await context.send(f"Error; {member} has too high of a role to be promoted.")
                break

    @commands.command(name='demote', aliases=['d'], help='Demotes given user')
    async def demote(self, context, member: str = 0):
        member_roles = context.author.roles
        phantom_server = self.discord_client.get_guild(364962599508508672)  # should = phantom guild id
        role_object = phantom_server.get_role(697605737999761408)  # should = veil id
        if role_object not in member_roles:
            await context.send(f'This command requires the ``VEIL`` role to be used.')
            return
        if member == 0:
            await context.send(f'{context.author.mention} Command syntax: `p?demote <member>`')
            return
        phantom_group = await roblox_client.get_group(3248486)
        member_object = await roblox_client.get_user(member)
        member_id = member_object.id
        while True:
            try:
                await phantom_group.demote(member_id)
                await context.send(f"{member} has been demoted by {context.author.mention}")
                break
            except robloxapi.utils.errors.NotFound:
                await context.send(f"Error; {member} couldn't be found in the group.")
                break
            except robloxapi.utils.errors.BadStatus:
                await context.send(f"Error; {member} has too high of a role to be promoted.")
                break


def setup(discord_client):
    discord_client.add_cog(roblox(discord_client))
