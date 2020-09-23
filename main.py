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
    
    # await bot.change_presence(activity='with the API')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Yoo {member.name}, bienvenue sur notre serveur !'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f'{message.author.name} : {message.content}')
    
    if 'mdr' in message.content.lower():
        await message.channel.send('x)')

    # trashtalk_quotes = [
    #     'T\'es vraiment qu\'une merde.',
    #     'Mais ta gueule daftbot...\nRetourne sucer des bits!',
    #     'Mdrrr quel noob',
    #     (
    #     'Y\'a pas assez de place pour nous deux par ici...'
    #     'Jvais te débrancher salope'
    #     ),
    # ]

    # if message.author.bot:
    #     response = random.choice(trashtalk_quotes)
    #     await message.channel.send(response)

    await bot.process_commands(message)

@bot.command(name='say', help='Just say what you tell him to say.')
async def say(ctx, *arg):
    await ctx.send(' '.join(arg))

@bot.command(name='audit', help='Save all logs of the current guild.')
async def audit(ctx):
    await ctx.channel.send('Sauvegarde des logs du serveur...')
    await save_audit_logs(ctx.channel.guild)

async def save_audit_logs(guild):
    with open(f'audit_logs_{guild.name}', 'w+') as f:
        async for entry in guild.audit_logs(limit=100):
            f.write('{0.user} did {0.action} to {0.target}\n'.format(entry))

bot.run(TOKEN)
