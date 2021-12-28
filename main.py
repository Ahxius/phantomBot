import os
from dotenv import load_dotenv
from discord.ext.commands import Bot, MinimalHelpCommand
from discord import Intents, Embed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = Intents.default()
intents.voice_states = True
intents.typing = True


client = Bot(command_prefix='p?', intents=intents)


class help_class(MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = Embed(description=page)
            await destination.send(embed=embed)


client.help_command = help_class()


for module in os.listdir('/home/ubuntu/phantomBot/modules'):
    if not module.endswith('.py'):
        continue
    try:
        client.load_extension(f'modules.{module[:-3]}')
    except SyntaxError as es:
        print(f'Failed to load module {module} due to a syntax error.')
    except ImportError as ei:
        print(f'Failed to load module {module} due to an import error.')


@client.event
async def on_ready():
    print(f'Discord login successful - {client.user}')


client.run(TOKEN)
