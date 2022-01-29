from discord.ext import commands
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from discord import Embed

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1mxGUjQkNnYPHEo40Kt8LYDzuS6--_6x_M4NRRhfFVIk'
RANGE_NAME = 'Logging Sheet!B7:F'
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()


class Sheets(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='checksheet', aliases=['info'])
    async def checksheet(self, context, *, user: str = None):
        if not user:
            await context.send('``p?checksheet <user>``')
            return
        status, ap, rp = get_info(user)
        if not status:
            await context.send('There was an error, please try again.')
            return
        embed = Embed(title=f"{user}'s Information")
        embed.add_field(name='AP', value=ap)
        embed.add_field(name='RP', value=rp)
        await context.send(embed=embed)

    @commands.command(name='addap', aliases=['ap'])
    async def addap(self, context, to_add: int, *users):
        member_roles = context.author.roles
        phantom_server = self.client.get_guild(364962599508508672)  # should = phantom guild id
        role_object = phantom_server.get_role(697605737999761408)  # should = veil id
        channel = phantom_server.get_channel(676604257905934399)
        if role_object not in member_roles and context.author.id != 193051160616239104:
            await context.send(f'This command requires the ``VEIL`` role to be used.')
            return
        if not users:
            await context.send('``p?addap <user>``')
            return
        users_success = []
        users_fail = []
        embed = Embed(title=f'AP added by {context.author.name}')
        for x in range(0, len(users)):
            status = update_info(f'{users[x]}', to_add, True)
            if status:
                users_success.append(f'{users[x]} ')
            else:
                users_fail.append(users[x])
        print(users_success, users_fail)
        embed.add_field(name='Success:', value=''.join(users_success))
        if len(users_fail) > 0:
            embed.add_field(name='Failure:', value=''.join(users_fail))
        await channel.send(embed=embed)
        await context.message.add_reaction('\U00002705')

    @commands.command(name='addrp', aliases=['rp'])
    async def addrp(self, context, to_add: int, *users):
        member_roles = context.author.roles
        phantom_server = self.client.get_guild(364962599508508672)  # should = phantom guild id
        role_object = phantom_server.get_role(697605737999761408)  # should = veil id
        channel = phantom_server.get_channel(676604257905934399)
        if role_object not in member_roles and context.author.id != 193051160616239104:
            await context.send(f'This command requires the ``VEIL`` role to be used.')
            return
        if not users:
            await context.send('``p?addrp <user>``')
            return
        users_success = []
        users_fail = []
        embed = Embed(title=f'RP added by {context.author.name}')
        for x in range(0, len(users)):
            status = update_info(f'{users[x]}', to_add, False)
            if status:
                users_success.append(f'{users[x]} ')
            else:
                users_fail.append(users[x])
        embed.add_field(name='Success:', value=''.join(users_success))
        if len(users_fail) > 0:
            embed.add_field(name='Failure:', value=''.join(users_fail))
        await channel.send(embed=embed)
        await context.message.add_reaction('\U00002705')


def get_info(username):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return False, None, None
    else:
        for row in values:
            if row[2] == username:
                return True, row[3], row[4]
        return False, None, None


def update_info(username, addamt, is_ap):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return False
    else:
        x = 6
        for row in values:
            x += 1
            if row[2] == str(username):
                valueInputOption = 'USER_ENTERED'
                if is_ap:
                    ap = float(row[3])
                    ap += addamt
                    body = {"values": [[str(ap)]]}
                    sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f'E{x}', body=body,
                                          valueInputOption=valueInputOption).execute()
                else:
                    rp = int(row[4][0:1])
                    rp += addamt
                    body = {"values": [[str(rp) + row[4][1:]]]}
                    sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f'F{x}', body=body,
                                          valueInputOption=valueInputOption).execute()
                return True
        return False


def setup(client):
    client.add_cog(Sheets(client))
