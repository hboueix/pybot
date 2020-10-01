from lib.config import Config
from lib.utils import *

import discord
from discord.ext import commands

PREFIX = Config().prefix


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help='Get help with a command or cog.\n eg. `!help utils`')
    async def help(self, ctx, page='Help'):
        page = page.capitalize()
        all_cogs = [c for c in self.bot.cogs]
        all_cogs.remove('Event')
        all_cogs = '`, `'.join(all_cogs)
        color = discord.Colour.green()
        if page in all_cogs:
            embed = discord.Embed(title=f'Help with {page} cog',
                                  description=self.bot.cogs[page].__doc__, color=color)

            embed.add_field(name=f'The current loaded cogs are (`{all_cogs}`) :gear:', value=f'**Cog commands**: '
                            f'{self.bot.description}')

            for c in self.bot.get_cog(page).get_commands():
                if await c.can_run(ctx):
                    if len(c.signature) == 0:
                        command = f'`{PREFIX}{c.name}`'
                    else:
                        command = f'`{PREFIX}{c.name} {c.signature}`'
                    if len(c.short_doc) == 0:
                        message = 'There is no documentation for this command'
                    else:
                        message = c.short_doc
                    embed.add_field(name=command, value=message, inline=False)
        else:
            all_commands = [c.name for c in self.bot.commands if await c.can_run(ctx)]
            page_lo = page.lower()
            if page_lo in all_commands:
                embed = discord.Embed(title=f'Help with the `{PREFIX}'
                                      f'{self.bot.get_command(page_lo)}` command', color=color)
                if len(self.bot.get_command(page_lo).help) == 0:
                    message = 'There is no documentation for this command'
                else:
                    message = self.bot.get_command(page_lo).help
                embed.add_field(name='Documentation:', value=message)

                if len(self.bot.get_command(page_lo).signature) != 0:
                    args = self.bot.get_command(page_lo).signature
                    embed.add_field(name='Arguments', value=f'`{args}`')
            else:
                embed = discord.Embed(title='Error!',
                                      description=f'**Error 404:** Command or Cog \"{help}\" not found ¯\_(ツ)_/¯',
                                      color=discord.Color.red())
                embed.add_field(
                    name=f'Current loaded Cogs are (`{all_cogs}`) :gear:', value='\u200b')

        await ctx.send(embed=embed)