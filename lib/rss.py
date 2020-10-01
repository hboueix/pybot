import feedparser

from lib.utils import getChannel

import discord

feed_url = "https://www.japscan.se/rss/solo-leveling/"

def getLastEntry():
	anime_feed = feedparser.parse(feed_url)
	entries = anime_feed.entries

	entry = entries[0]

	entry = embed_entry(entry)

	# for key in anime_feed.keys():
	# 	if key != 'entries':
	# 		print(f'{key} : {anime_feed[key]}')
	# for key in entry.keys():
	# 	print(f'{key} : {entry[key]}')

	return entry


def embed_entry(entry):
	embed = discord.Embed(title=entry.title, url=entry.link, color=0x2b14f3)

	embed.set_thumbnail(url="https://www.japscan.se/imgs/mangas/solo-leveling.jpg")
	embed.add_field(name="Go le lire", value=entry.link, inline=False)

	return embed
	
