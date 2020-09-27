import datetime
import random

VERSION = '1.0.0'
CONFIG = './config.txt'
INIT_TIME = datetime.datetime.now()


def getFromConfigFile(var):
    with open(CONFIG) as f:
        lines = f.read().splitlines()

    for line in lines:
        if line.startswith(var):
            return line.split('=')[1]


def save_commands_logs(bot, ctx):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    with open(f'commands_logs_{bot.user.name}', 'a') as f:
        f.write(f"{now} {ctx.message.author} exec: {ctx.message.content}\n")


def save_msg_logs(bot, ctx):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    with open(f'msg_logs_{bot.user.name}', 'a') as f:
        f.write(f"{now} reply to: {ctx.message.content}\n")


def winOrFail(delimiter):
    return True if random.random() < float(delimiter) else False
