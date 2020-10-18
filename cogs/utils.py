import random
import time
import datetime
import asyncio

import discord
from discord.ext import commands


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # region commands
    @commands.command(name='choose', help='Random choice one between all inputs.')
    async def choose(self, ctx, *args):
        response = f'... J\'ai fait mon choix :\n => {random.choice(args)}'
        await ctx.send(response)

    @commands.command(name='say', help='Just say what you tell him to say.')
    async def say(self, ctx, *arg):
        await ctx.message.delete()
        response = ' '.join(arg)
        await ctx.send(response)
        self.save_commands_logs(self.bot, ctx)

    @commands.command(name='vote', help='Create a poll about what you give in arguments.')
    async def vote(self, ctx, question, time_to_vote: int = 3):
        await ctx.message.delete()

        good_emojis = ['\u2705', '\u26D4']
        member = ctx.message.author
        embed = discord.Embed(
            title=question, color=discord.Colour.gold()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Réponses possibles :', value='\u2705 Oui \u26D4 Non')
        embed.set_footer(text=f'\u231B {time_to_vote}min')
        msg = await ctx.send(embed=embed)

        await msg.add_reaction(emoji='\u2705')# :white_check_mark:
        await msg.add_reaction(emoji='\u26D4')# :no_entry:

        await asyncio.sleep(time_to_vote * 60)

        msg = await ctx.fetch_message(msg.id)
        reactions_count = {reaction.emoji: reaction.count for reaction in msg.reactions}
        await msg.delete()

        result = ""
        for emoji, react_count in reactions_count.items():
            if emoji not in good_emojis:
                reactions_count.pop(emoji)
            else:
                result += f"{emoji} {react_count - 1}\n"

        # winner = max(reactions_count, key=reactions_count.get)
        # max_count = reactions_count.pop(winner)

        # if max(reactions_count.values()) == max_count:
        #     winner = None

        embed = discord.Embed(
            title="Résultat du vote", color=discord.Colour.gold()
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Réponses :', value=result)
        embed.set_footer(text=f'a demandé "{question}"', icon_url=member.avatar_url)

        await ctx.send(embed=embed)
    # endregion

    # region methods
    def save_commands_logs(self, bot, ctx):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        with open(f'log/commands_{bot.user.name}.log', 'a') as log_file:
            log_file.write(
                f"[{now}] {ctx.message.author} exec: {ctx.message.content}\n")
    # endregion
