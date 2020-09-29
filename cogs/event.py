import datetime

import discord
from discord.ext import commands

from lib.utils import *


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Yoo {member.name}, bienvenue sur notre serveur !'
        )

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

        if message.content[0] != self.bot.command_prefix:
            for key, value in fast_answer.items():
                if key in message.content.lower() and winOrFail(0.3):
                    await message.channel.send(value)
                    await save_msg_logs(self.bot, message)
                    break

        trashtalk_quotes = [
            'T\'es vraiment qu\'une merde.',
            'Mais ta gueule daftbot...\nRetourne sucer des bits!',
            'Mdrrr quel noob',
            (
                'Y\'a pas assez de place pour nous deux par ici...'
                'Jvais te débrancher salope'
            ),
        ]

        if message.author.bot and message.author.name == 'daftbot' and winOrFail(0.3):
            response = random.choice(trashtalk_quotes)
            await message.channel.send(response)
