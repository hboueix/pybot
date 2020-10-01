import os

from lib.utils import *
from lib.config import Config

import discord
from discord.ext import commands

from cogs.event import Event
from cogs.admin import Admin
from cogs.utils import Utils
from cogs.help import Help

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

config = Config()
TOKEN = config.token
PREFIX = config.prefix

bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')

bot.add_cog(Event(bot))
bot.add_cog(Admin(bot))
bot.add_cog(Utils(bot))
bot.add_cog(Help(bot))

bot.run(TOKEN)
