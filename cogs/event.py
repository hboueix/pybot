import datetime
import asyncio
import random
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import feedparser

import discord
from discord.ext import commands


class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.background_task())

    # region listeners
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
                if key in message.content.lower() and self.win_or_fail(0.3):
                    await message.channel.send(value)
                    await self.save_msg_logs(self.bot, message)
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

        if message.author.bot and message.author.name == 'daftbot' and self.win_or_fail(0.3):
            response = f'{message.author.mention} ' + \
                random.choice(trashtalk_quotes)
            await message.channel.send(response)
    # endregion

    # region methods
    async def background_task(self):
        await self.bot.wait_until_ready()

        last_entry = self.get_last_entry()
        is_last_entry_vf = await self.check_VF(last_entry.url)
        channel = self.get_channel(self.bot, 'news-anime')

        while not self.bot.is_closed():
            now = datetime.datetime.now()

            if now.weekday() in (2, 3):
                update = self.get_last_entry()
                is_update_vf = await self.check_VF(update.url)
                if is_update_vf and not is_last_entry_vf:
                    last_entry = update
                    is_last_entry_vf = is_update_vf
                    await channel.send("@here", embed=last_entry)
                elif update.title != last_entry.title:
                    last_entry = update
                    is_last_entry_vf = is_update_vf
                    if is_update_vf:
                        await channel.send("@here", embed=last_entry)

            await asyncio.sleep(10)

    async def check_VF(self, link):
        headers = { 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) \
                            Gecko/20100101 Firefox/81.0',
        }
        page = urlopen(Request(link, headers=headers))
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")
        note = soup.find_all("div", id="note")

        if len(note) > 0:
            if 'RAW' in note[0]:
                return False

        return True

    def get_last_entry(self):
        feed_url = "https://www.japscan.se/rss/solo-leveling/"
        img_url = "https://www.japscan.se/imgs/mangas/solo-leveling.jpg"
        anime_feed = feedparser.parse(feed_url)

        entries = anime_feed.entries
        entry = entries[0]

        embed = discord.Embed(
            title=entry.title, url=entry.link, color=0x2b14f3)
        embed.add_field(name="Go le lire", value=entry.link, inline=False)
        embed.set_thumbnail(url=img_url)

        # for key in anime_feed.keys():
        # 	if key != 'entries':
        # 		print(f'{key} : {anime_feed[key]}')
        # for key in entry.keys():
        # 	print(f'{key} : {entry[key]}')

        return embed

    def win_or_fail(self, delimiter):
        return True if random.random() < float(delimiter) else False

    def get_channel(self, bot, channel_name):
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.name == channel_name:
                    return channel

    def save_msg_logs(self, bot, msg):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        with open(f'log/msg_{bot.user.name}.log', 'a') as log_file:
            log_file.write(
                f"[{now}] reply: {msg.content} | to: {msg.author}\n")
    # endregion
