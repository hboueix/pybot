import datetime
import asyncio

import discord
from discord.ext import commands

from lib.utils import *
from lib.rss import getLastEntry


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.background_task())

    async def background_task(self):
        await self.bot.wait_until_ready()

        last_entry = getLastEntry()
        channel = getChannel(self.bot, 'bot-room')

        while not self.bot.is_closed():
            now = datetime.datetime.now()

            if now.weekday() in (2, 3):
                update = getLastEntry()
                if update.title != last_entry.title:
                    last_entry = update
                    await channel.send("@here", embed=last_entry)
      
            await asyncio.sleep(1800)

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f'{self.bot.user} has connected to Discord!\n'
        )

        for guild in self.bot.guilds:
            members = '\n - '.join(
                [f"{member.name} (id: {member.id})" for member in guild.members])
            print(
                f'{guild.name} (id: {guild.id})\n'
                f'Guild Members:\n - {members}\n'
            )

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     await member.create_dm()
    #     await member.dm_channel.send(
    #         f'Yoo {member.name}, bienvenue sur notre serveur !'
    #     )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f'[{now}] {message.author.name} : {message.content}')

        fast_answer = {
            'mdr': 'x)',
            'gg': 't\'es vraiment trop fort mec'
        }

        if len(message.content) > 0 and message.content[0] != self.bot.command_prefix:
            for key, value in fast_answer.items():
                if key in message.content.lower() and winOrFail(0.3):
                    await message.channel.send(value)
                    await save_msg_logs(self.bot, message)
                    break

        trashtalk_quotes = [
            'T\'es vraiment qu\'une merde.',
            'Mais ta gueule...\nRetourne sucer des bits!',
            'Mdrrr t\'es vraiment un noob',
            (
                'Y\'a pas assez de place pour nous deux par ici...'
                'Jvais te débrancher salope'
            ),
        ]

        if message.author.bot and message.author.name == 'daftbot' and winOrFail(0.3):
            response = f'{message.author.mention} ' + random.choice(trashtalk_quotes)
            await message.channel.send(response)
