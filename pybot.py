import logging
from discord import Intents
from discord.ext import commands

from config import Config

from cogs.event import Event
from cogs.admin import Admin
from cogs.utils import Utils
from cogs.info import Info
from cogs.leekwars import Leekwars
from cogs.help import Help

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = Intents.default()
intents.members, intents.presences = True, True  # Subscribe to the privileged members intent.S
bot = commands.Bot(command_prefix=Config['COMMANDS_PREFIX'], intents=intents)
bot.remove_command('help')

bot.add_cog(Event(bot))
bot.add_cog(Admin(bot))
bot.add_cog(Utils(bot))
bot.add_cog(Info(bot))
bot.add_cog(Leekwars(bot))
bot.add_cog(Help(bot))

bot.run(Config['DISCORD_TOKEN'])
