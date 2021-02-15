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


class sheets(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='getinfo', aliases=['info', 'ap', 'rp'])
    async def getinfo(self, context, user: str = None):
        if not user:
            await context.send('``p?getinfo <user>``')
            return
        status, ap, rp = get_info(user)
        if not status:
            await context.send('There was an error, please try again.')
            return
        embed = Embed(title=f"{user}'s Information")
        embed.add_field(name='AP', value=ap)
        embed.add_field(name='RP', value=rp)
        await context.send(embed=embed)


def get_info(username):
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
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return False, None, None
    else:
        for row in values:
            if row[2] == username:
                # Returns AP and RP
                return True, row[3], row[4]
        return False, None, None


def setup(client):
    client.add_cog(sheets(client))
