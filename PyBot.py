import os

from lib.utils import *

import discord
from discord.ext import commands

from cogs.event import Event
from cogs.admin import Admin

TOKEN = getFromConfigFile('DISCORD_TOKEN')
PREFIX = getFromConfigFile('COMMANDS_PREFIX')

bot = commands.Bot(command_prefix=PREFIX)

bot.add_cog(Event(bot))
bot.add_cog(Admin(bot))

bot.run(TOKEN)
