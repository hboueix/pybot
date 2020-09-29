import datetime
import random

from lib.config import Config

import discord
from discord.ext import commands

VERSION = '1.1.0'
INIT_TIME = datetime.datetime.now()


def userIsOwner():
    def predicate(ctx):
        print(ctx)
        return True if ctx.message.author.id == getOwnerId() else False
    return commands.check(predicate)


def getOwnerId():
    return int(Config().owner_id)


async def alertWrongPerms(ctx):
    await ctx.channel.send('Vous n\'avez pas accès à cette commande !')


def save_commands_logs(bot, ctx):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    with open(f'log/commands_{bot.user.name}.log', 'a') as f:
        f.write(f"[{now}] {ctx.message.author} exec: {ctx.message.content}\n")


def save_commands_refused_logs(bot, ctx):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    with open(f'log/commands_refused_{bot.user.name}.log', 'a') as f:
        f.write(f"[{now}] {ctx.message.author} tried to exec: {ctx.message.content}\n")


def save_msg_logs(bot, msg):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    with open(f'log/msg_{bot.user.name}.log', 'a') as f:
        f.write(f"[{now}] reply: {msg.content} | to: {msg.author}\n")


def winOrFail(delimiter):
    return True if random.random() < float(delimiter) else False
