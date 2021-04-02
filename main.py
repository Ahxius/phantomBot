import os
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord import Intents

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = Intents.default()
intents.voice_states = True


client = Bot(command_prefix='lizardsucks!', intents=intents)

for cog in os.listdir('modules'):
    if not cog.endswith('.py'):
        continue
    try:
        client.load_extension(f'modules.{cog[:-3]}')
    except SyntaxError as es:
        print(f'Failed to load module {cog} due to a syntax error.')
    except ImportError as ei:
        print(f'Failed to load module {cog} due to an import error.')


@client.event
async def on_ready():
    print(f'Discord login successful - {client.user}')


client.run(TOKEN)
