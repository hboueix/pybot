import datetime

import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prefix = self.bot.command_prefix

    # region commands
    @commands.command(name='help', help='Get help with a command or cog.\n eg. `!help utils`')
    async def help(self, ctx, page='Help'):
        page = page.capitalize()
        all_cogs = list(c for c in self.bot.cogs)
        all_cogs.remove('Event')
        all_cogs = '`, `'.join(all_cogs)
        color = discord.Colour.green()
        if page in all_cogs:
            embed = discord.Embed(
                title=f'Help with {page} cog',
                description=self.bot.cogs[page].__doc__, color=color)

            embed.add_field(
                name=f'The current loaded command categories are (`{all_cogs}`) :gear:',
                value=f'**Cog commands**: '
                f'{self.bot.description}')

            for cog in self.bot.get_cog(page).get_commands():
                if await cog.can_run(ctx):
                    if len(cog.signature) == 0:
                        command = f'`{self.prefix}{cog.name}`'
                    else:
                        command = f'`{self.prefix}{cog.name} {cog.signature}`'
                    if len(cog.short_doc) == 0:
                        message = 'There is no documentation for this command'
                    else:
                        message = cog.short_doc
                    embed.add_field(name=command, value=message, inline=False)
        else:
            all_commands = [c.name for c in self.bot.commands if await c.can_run(ctx)]
            page_lo = page.lower()
            if page_lo in all_commands:
                embed = discord.Embed(title=f'Help with the `{self.prefix}'
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
                desc = fr'**Error 404:** Command or Cog \"{page.lower()}\" not found ¯\_(ツ)_/¯'
                embed = discord.Embed(
                    title='Error!',
                    description=desc,
                    color=discord.Color.red())
                embed.add_field(
                    name=f'Current loaded Cogs are (`{all_cogs}`) :gear:', value='\u200b')

        await ctx.send(embed=embed)
    # endregion

    # region methods
    def save_commands_logs(self, bot, ctx):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        with open(f'log/commands_{bot.user.name}.log', 'a') as log_file:
            log_file.write(
                f"[{now}] {ctx.message.author} exec: {ctx.message.content}\n")
    # endregion
