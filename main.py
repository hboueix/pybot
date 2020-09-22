# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    #guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} has connected to Discord!\n'
    )

    for guild in bot.guilds:
        members = '\n - '.join([f"{member.name} (id: {member.id})" for member in guild.members])
        print(
            f'{guild.name} (id: {guild.id})\n'
            f'Guild Members:\n - {members}\n'
        )

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Yoo {member.name}, bienvenu sur notre serveur !'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if 'mdr' in message.content.lower():
        await message.channel.send('x)')


    trashtalk_quotes = [
        'T\'es vraiment qu\'une merde.',
        'Mais ta gueule daftbot...\nRetourne sucer des bits!',
        'Mdrrr quel noob',
        (
        'Y\'a pas assez de place pour nous deux par ici...'
        'Jvais te débrancher salope'
        ),
    ]

    if message.author.bot:
        response = random.choice(trashtalk_quotes)
        await message.channel.send(response)

bot.run(TOKEN)
