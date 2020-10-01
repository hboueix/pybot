import discord
from discord.ext import commands

from lib.utils import *


class Admin(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.status = None
		self.activity = None

	async def cog_check(self, ctx):
		if ctx.message.author.id == getOwnerId():
			check = True
		else:
			await alertWrongPerms(ctx)
			await save_commands_refused_logs(self, ctx)
			check = False
		return check

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

	@commands.command(name='status', help='Set bot status.')
	async def status(self, ctx, state=None):
		await ctx.message.delete()
		if await self.setStatus(state):
			response = 'Statut mis à jour !'
		else:
			response = 'Ce statut n\'est pas valide !\nEssaye avec :\n- idle\n- invisible\n- offline\n- online\n- dnd'
		await ctx.channel.send(response)
		save_commands_logs(self.bot, ctx)

	@commands.command(name='activity', help='Set bot activity.')
	async def activity(self, ctx, action=None, onwhat=None, url=None):
		await ctx.message.delete()
		if await self.setActivity(action, onwhat, url):
			response = 'Activité mise à jour !'
		else:
			response = 'Cette activité n\'est pas valide !\nEssaye avec :\n- play\n- stream\n- listen\n- watch'
		await ctx.channel.send(response)
		save_commands_logs(self.bot, ctx)
 
	@commands.command(name='say', help='Just say what you tell him to say.')
	async def say(self, ctx, *arg):
		await ctx.message.delete()
		response = ' '.join(arg)
		await ctx.send(response)
		save_commands_logs(self.bot, ctx)

	@commands.command(name='uptime', help='Get bot uptime.')
	async def uptime(self, ctx):
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
		save_commands_logs(self.bot, ctx)

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
		save_commands_logs(self.bot, ctx)

	@commands.command(name='version', help='Display bot version.')
	async def version(self, ctx):
		await ctx.message.delete()
		await ctx.send(f'{self.bot.user.name} v{VERSION}')
		save_commands_logs(self.bot, ctx)
