from lib.config import Config
from lib.utils import *

import discord
from discord.ext import commands

PREFIX = Config().prefix


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='choose', help='Random choice one between all inputs.')
    async def choose(self, ctx, *args):
        response = f'... J\'ai fait mon choix :\n => {random.choice(args)}'
        await ctx.send(response)
