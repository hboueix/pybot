import datetime

import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status = None
        self.activity = None

    async def cog_check(self, ctx):
        if ctx.message.author.id == self.getOwnerId():
            check = True
        else:
            await self.alertWrongPerms(ctx)
            await self.save_commands_refused_logs(self.bot, ctx)
            check = False
        return check

    # region commands
    @commands.command(name='status', help='Set bot status.')
    async def _status(self, ctx, state=None):
        await ctx.message.delete()
        if await self.setStatus(state):
            response = 'Statut mis à jour !'
        else:
            response = 'Ce statut n\'est pas valide !\nEssaye avec :\n- idle\n- invisible\n- offline\n- online\n- dnd'
        await ctx.channel.send(response)
        self.save_commands_logs(self.bot, ctx)

    @commands.command(name='activity', help='Set bot activity.')
    async def _activity(self, ctx, action=None, onwhat=None, url=None):
        await ctx.message.delete()
        if await self.setActivity(action, onwhat, url):
            response = 'Activité mise à jour !'
        else:
            response = 'Cette activité n\'est pas valide !\nEssaye avec :\n- play\n- stream\n- listen\n- watch'
        await ctx.channel.send(response)
        self.save_commands_logs(self.bot, ctx)

    @commands.command(name='purge', help='Remove messages.')
    async def purge(self, ctx, amount=None):
        await ctx.message.delete()
        if amount == 'all':
            await ctx.channel.purge()
        elif amount == None:
            await ctx.channel.purge(limit=1)
        else:
            try:
                await ctx.channel.purge(limit=int(amount))
            except Exception as e:
                await ctx.send(f'An error occurred while processing this request: ```py\n{type(e).__name__}: {e}\n```')

    @commands.command(name='audit', help='Save all logs of the current guild.')
    async def audit(self, ctx):
        await ctx.message.delete()
        await ctx.channel.send('Sauvegarde des logs du serveur...')
        guild = ctx.channel.guild
        with open(f'log/audit_{guild.name}.log', 'w+') as f:
            async for entry in guild.audit_logs(limit=100):
                f.write(
                    f'{entry.user} did {entry.action} to {entry.target}\n'
                )
        self.save_commands_logs(self.bot, ctx)
    # endregion

    # region methods
    async def setStatus(self, state):
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
            self.status = status
            await self.bot.change_presence(status=self.status, activity=self.activity)
            return True

    async def setActivity(self, action, onwhat, url):
        all_activities = {
            'play': discord.Game(name=onwhat, type=3),
            'stream': discord.Streaming(name=onwhat, url=url),
            'listen': discord.Activity(type=discord.ActivityType.listening, name=onwhat),
            'watch': discord.Activity(type=discord.ActivityType.watching, name=onwhat),
            'none': None
        }
        activity = all_activities.get(action, 'NOT FOUND')

        if activity == 'NOT FOUND':
            return False
        else:
            self.activity = activity
            await self.bot.change_presence(status=self.status, activity=self.activity)
            return True

    async def alertWrongPerms(self, ctx):
        await ctx.channel.send('Vous n\'avez pas accès à cette commande !')

    def getOwnerId(self):
        with open('../config.py', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('OWNER_ID'):
                    return int(line.split(': ')[1])

    def save_commands_logs(self, bot, ctx):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        with open(f'log/commands_{bot.user.name}.log', 'a') as f:
            f.write(
                f"[{now}] {ctx.message.author} exec: {ctx.message.content}\n")

    def save_commands_refused_logs(self, bot, ctx):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        with open(f'log/commands_refused_{bot.user.name}.log', 'a') as f:
            f.write(
                f"[{now}] {ctx.message.author} tried to exec: {ctx.message.content}\n")
    # endregion
