import os
import random
import datetime

from lib.config import Config

import discord
from discord.ext import commands

config = Config()
TOKEN = config.token
PREFIX = config.prefix

bot = commands.Bot(command_prefix=PREFIX)

VERSION = '1.0.0'
STATUS = None
ACTIVITY = None
INIT_TIME = datetime.datetime.now()

# region events


@bot.event
async def on_ready():
    print(
        f'{bot.user} has connected to Discord!\n'
    )

    for guild in bot.guilds:
        members = '\n - '.join(
            [f"{member.name} (id: {member.id})" for member in guild.members])
        print(
            f'{guild.name} (id: {guild.id})\n'
            f'Guild Members:\n - {members}\n'
        )


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

    fast_answer = {
        'mdr': 'x)',
        'gg': 't\'es vraiment trop fort mec'
    }

    if message.content[0] != PREFIX:
        for key, value in fast_answer.items():
            if key in message.content.lower() and winOrFail(0.5):
                await message.channel.send(value)
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

    await bot.process_commands(message)
# endregion

# region commands


@bot.command(name='version', help='Display bot version.')
async def version(ctx):
    await ctx.message.delete()
    await ctx.send(f'{bot.user.name} v{VERSION}')
    save_commands_logs(f'{ctx.message.author} exec: {PREFIX}version')


@bot.command(name='say', help='Just say what you tell him to say.')
async def say(ctx, *arg):
    await ctx.message.delete()
    response = ' '.join(arg)
    await ctx.send(response)
    save_commands_logs(f'{ctx.message.author} exec: {PREFIX}say {response}')


@bot.command(name='audit', help='Save all logs of the current guild.')
async def audit(ctx):
    await ctx.message.delete()
    await ctx.channel.send('Sauvegarde des logs du serveur...')
    await save_audit_logs(ctx.channel.guild)
    save_commands_logs(f'{ctx.message.author} exec: {PREFIX}audit')


@bot.command(name='uptime', help='Get bot uptime.')
async def uptime(ctx):
    await ctx.message.delete()
    start = INIT_TIME
    uptime = datetime.datetime.now() - start
    months = {
        1: 'Janvier',
        2: 'Février',
        3: 'Mars',
        4: 'Avril',
        5: 'Mai',
        6: 'Juin',
        7: 'Juillet',
        8: 'Août',
        9: 'Septembre',
        10: 'Octobre',
        11: 'Novembre',
        12: 'Décembre'
    }
    await ctx.channel.send(
        f'Je tourne depuis le {start.day} {months[start.month]} {start.year} ({start.hour}h{start.minute}).\n'
        f'Soit depuis {uptime.days} jour(s), {uptime.seconds//3600} heure(s), {(uptime.seconds%3600)//60} minute(s) et {(uptime.seconds%3600)%60} seconde(s).'
    )
    save_commands_logs(f'{ctx.message.author} exec: {PREFIX}uptime')


@bot.command(name='status', help='Set bot status.')
async def status(ctx, state=None):
    await ctx.message.delete()
    if await setStatus(state):
        response = 'Statut mis à jour !'
    else:
        response = 'Ce statut n\'est pas valide !\nEssaye avec :\n- idle\n- invisible\n- offline\n- online\n- dnd'
    await ctx.channel.send(response)


@bot.command(name='activity', help='Set bot activity.')
async def activity(ctx, action=None, onwhat=None, url=None):
    await ctx.message.delete()
    if await setActivity(action, onwhat, url):
        response = 'Activité mise à jour !'
    else:
        response = 'Cette activité n\'est pas valide !\nEssaye avec :\n- play\n- stream\n- listen\n- watch'
    await ctx.channel.send(response)
# endregion

# region functions


async def setActivity(action, onwhat, url):
    global STATUS
    global ACTIVITY
    all_activities = {
        'play': discord.Game(name=onwhat, type=3),
        'stream': discord.Streaming(name=onwhat, url=url),
        'listen': discord.Activity(type=discord.ActivityType.listening, name=onwhat),
        'watch': discord.Activity(type=discord.ActivityType.watching, name=onwhat)
    }
    activity = all_activities.get(action, 'NOT FOUND')

    if activity == 'NOT FOUND':
        return False
    else:
        ACTIVITY = activity
        await bot.change_presence(status=STATUS, activity=activity)
        return True


async def setStatus(state):
    global STATUS
    global ACTIVITY
    all_status = {
        'idle': discord.Status.idle,
        'invisible': discord.Status.invisible,
        'offline': discord.Status.offline,
        'online': discord.Status.online,
        'dnd': discord.Status.do_not_disturb
    }
    status = all_status.get(state, 'NOT FOUND')

    if status == 'NOT FOUND':
        return False
    else:
        STATUS = status
        await bot.change_presence(status=status, activity=ACTIVITY)
        return True


async def save_audit_logs(guild):
    with open(f'audit_logs_{guild.name}', 'w+') as f:
        async for entry in guild.audit_logs(limit=100):
            f.write(f'{entry.user} did {entry.action} to {entry.target}\n')


def save_commands_logs(entry):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    with open(f'commands_logs_{bot.user.name}', 'a') as f:
        f.write(now + ' ' + entry + '\n')


def save_msg_logs(entry):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    with open(f'msg_logs_{bot.user.name}', 'a') as f:
        f.write(now + ' ' + entry + '\n')


def winOrFail(delimiter):
    return True if random.random() < float(delimiter) else False
# endregion


bot.run(TOKEN)
