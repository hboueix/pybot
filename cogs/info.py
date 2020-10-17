import datetime
import subprocess

import discord
from discord.ext import commands


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.init_time = datetime.datetime.now()

    # region commands
    @commands.command(name='ping', help='Get bot latency.')
    async def ping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"{self.bot.user.name}'s latency: {self.bot.latency * 1000:.0f}ms")

    @commands.command(name='uptime', help='Get bot uptime.')
    async def uptime(self, ctx):
        await ctx.message.delete()
        start = self.init_time
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
            f'Je tourne depuis le {start.day} {months[start.month]} {start.year} '
            f'({start.hour}h{start.minute}).\n'
            f'Soit depuis {uptime.days} jour(s), {uptime.seconds//3600} heure(s), '
            f'{(uptime.seconds%3600)//60} minute(s) et {(uptime.seconds%3600)%60} seconde(s).')
        self.save_commands_logs(self.bot, ctx)

    @commands.command(name='version', help='Display bot version.')
    async def version(self, ctx):
        await ctx.message.delete()
        cmd = 'git describe --tags'.split()
        try:
            version = subprocess.check_output(cmd).decode().strip()
            version = version.split('-')[0]
            response = f'{self.bot.user.name} {version}'
        except subprocess.CalledProcessError:
            response = 'Unable to get version number from git tags.'
        finally:
            await ctx.send(response)
            self.save_commands_logs(self.bot, ctx)

    @commands.command(name='userinfo', help='Give infos about user.')
    async def userinfo(self, ctx, user=None):
        if user is None:
            member = ctx.message.author
        else:
            user = str(user)
            member = ctx.message.guild.get_member_named(user)

        if member is None:
            await ctx.message.delete()
            await ctx.channel.send(f"{ctx.message.author.mention} L'utilisateur {user} est inconnu")
        else:
            await ctx.message.delete()
            tmp = await ctx.channel.send("Chargement des informations...")

            try:
                title = f"Userinfo for {member.name}#{member.discriminator} [{member.top_role}]:"
                roles_list = self.get_list_user_roles(member)
                created_at = self.date_converter(member.created_at)
                joined_at = self.date_converter(member.joined_at)
                status = str(member.status)
                status_final = status.capitalize() if status != 'dnd' else 'Do not disturb'

                user_embed = discord.Embed()
                user_embed.title = title
                user_embed.colour = 0x3498db
                user_embed.set_thumbnail(url=member.avatar_url)
                user_embed.add_field(name="Nickname", value=member.nick)
                user_embed.add_field(name="ID", value=member.id)
                user_embed.add_field(name="Discriminator",
                                     value=member.discriminator)
                user_embed.add_field(name='Status', value=status_final)
                if hasattr(member, 'game'):
                    user_embed.add_field(name='Playing', value=member.game)
                user_embed.add_field(
                    name='Account created on', value=created_at)
                user_embed.add_field(name='Join server on', value=joined_at)
                user_embed.add_field(name="Roles", value=', '.join(roles_list))
                user_embed.set_footer(
                    text=f"Requested by {ctx.message.author.name}",
                    icon_url=ctx.message.author.avatar_url)

                await tmp.delete()
                await ctx.channel.send(embed=user_embed)

            except Exception as error:
                await ctx.channel.send(f'An error occurred while processing this request: ```py\n'
                                       f'{type(error).__name__}: {error}\n```')

    @commands.command(name='serverinfo', help='Give info about current server.')
    async def serverinfo(self, ctx):
        guild = ctx.message.guild
        await ctx.message.delete()
        tmp = await ctx.channel.send('Processing request...')
        verify_level = str(guild.verification_level)

        server_embed = discord.Embed()
        server_embed.colour = 0x3498db
        server_embed.set_thumbnail(url=guild.icon_url)
        server_embed.add_field(name="Server Name", value=guild.name)
        server_embed.add_field(name="Server ID", value=guild.id)
        server_embed.add_field(name="Owner's Name", value=guild.owner.name)
        server_embed.add_field(name="Owner's ID", value=guild.owner.id)
        server_embed.add_field(name="Text Channels",
                               value=str(len(self.get_list_channels(guild, 'text'))))
        server_embed.add_field(name="Voice Channels",
                               value=str(len(self.get_list_channels(guild, 'voice'))))
        server_embed.add_field(name="Users", value=guild.member_count)
        server_embed.add_field(name="Verification level",
                               value=verify_level.upper())
        # server_embed.add_field(name="Roles Count",
        # 					   value=str(len(guild.role_hierarchy)))
        # server_embed.add_field(name="Region",
        # 					   value=formatServerRegion(guild.region))
        server_embed.add_field(name="Creation Date",
                               value=self.date_converter(guild.created_at))
        server_embed.add_field(name="Emotes Count",
                               value=str(len(guild.emojis)))
        # server_embed.add_field(name="Roles",
        # 					   value=formatServerRoles(guild.role_hierarchy), inline=False)
        # server_embed.add_field(name="Emojis",
        # 					   value=formatEmojis(guild.emojis), inline=False)
        server_embed.set_footer(
            text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)

        await tmp.delete()
        await ctx.send(embed=server_embed)
    # endregion

    # region methods
    def date_converter(self, date):
        return date.strftime("%a %d %b %Y at %H:%M:%S")

    def get_list_user_roles(self, user):
        roles = user.roles
        list_roles = []
        for role in roles:
            list_roles.append(role.name)
        return list_roles

    def get_list_channels(self, guild, chan_type):
        channels = guild.channels
        list_channels = []
        for channel in channels:
            if str(channel.type) == chan_type:
                list_channels.append(channel)
        return list_channels

    def save_commands_logs(self, bot, ctx):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        with open(f'log/commands_{bot.user.name}.log', 'a') as log_file:
            log_file.write(
                f"[{now}] {ctx.message.author} exec: {ctx.message.content}\n")
    # endregion
