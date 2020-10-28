from random import randint

import requests
import requests_async as arequests
import asyncio

import discord
from discord.ext import commands


class LeekWars(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.connected_users = dict()

    @commands.command(name='login', help='Login to LeekWars API')
    async def connect(self, ctx):
        await ctx.message.delete()
        member = ctx.author
        await member.create_dm()
        all_dm = []
        all_dm.append(await member.dm_channel.send(
            "Quel est votre login LeekWars ?")
        )
        login = await self.bot.wait_for('message',
                                        check=lambda message: check_dm_channel(
                                            message, member),
                                        timeout=120)
        all_dm.append(await member.dm_channel.send(
            "Quel est votre mot de passe ?")
        )
        password = await self.bot.wait_for('message',
                                           check=lambda message: check_dm_channel(
                                               message, member),
                                           timeout=120)
        for dm in all_dm:
            await dm.delete()

        req = requests.post("https://leekwars.com/api/farmer/login-token",
                            data={"login": login.content, "password": password.content})
        response = req.json()
        if 'error' in response.keys():
            await member.dm_channel.send("Identifiants invalides.\nErreur : {response}")
        else:
            self.connected_users[member.id] = response
            await member.dm_channel.send("Vous êtes désormais connecté !")

        await member.dm_channel.send(
            "Noubliez pas de supprimer vos identifiants (au-dessus) juste au cas où..."
        )

    @commands.command(name='fight', help='Start LeekWars fights.')
    async def fight(self, ctx, leek=None, count=None):
        member = ctx.message.author
        if member.id not in self.connected_users.keys():
            return

        token = self.connected_users[member.id]['token']
        self.connected_users[member.id]['farmer'] = farmer = get_farmer(token)
        headers = get_headers(token)
        leeks = farmer['leeks']
        leek_names = [leek['name'] for leek in leeks.values()]
        choices = "\n".join(
            [f" - {leek}" for idx, leek in enumerate(leek_names)])
        fights = farmer['fights']

        if leek is None:
            await ctx.send(f"Choisissez votre poireau :\n{choices}")
            msg_leek = await self.bot.wait_for('message',
                                               check=lambda message: check_good_channel(
                                                   message, ctx),
                                               timeout=120)
            leek = msg_leek.content
        if leek.lower() not in map(str.lower, leek_names):
            await ctx.send(f"Le choix '{leek}' n'est pas valide. Recommencez")
            return
        else:
            leek_id = [idx for idx, val in leeks.items(
            ) if val['name'].lower() == leek.lower()][0]
        if count is None:
            await ctx.send(f"Combien ? (max: {fights})")
            msg_count = await self.bot.wait_for('message',
                                                check=lambda message: check_good_channel(
                                                    message, ctx),
                                                timeout=120)
            count = int(msg_count.content)
        if count not in range(fights+1):
            await ctx.send(f"Le choix '{count}' n'est pas valide. Recommencez")
            return

        fight_results = await run_fights(headers, leek_id, count, farmer['id'])
        s = 's' if count > 1 else ''
        await ctx.send(f"Combat{s} terminé{s} !")
        await self.fight_results(ctx, fight_results)

    async def fight_results(self, ctx, results):
        member = ctx.message.author
        farmer_id = self.connected_users[member.id]['farmer']['id']
        wins = results['win']
        looses = results['loose']
        ties = results['tie']
        s = 's' if results['total'] > 1 else ''
        embed = discord.Embed(
            title=f"Résultats combat{s}",
            description=f"Combat{s} lancé{s} : {results['total']}",
            color=discord.Color.green()
        )
        embed.add_field(
            name=f"\nVictoire{'s' if wins > 1 else ''}", value=wins, inline=True)
        embed.add_field(
            name=f"\nDéfaite{'s' if looses > 1 else ''}", value=looses, inline=True)
        embed.add_field(
            name=f"\nEgalité{'s' if ties > 1 else ''}", value=ties, inline=True)
        embed.set_footer(
            text=f"Requested by {member.name}",
            icon_url=member.avatar_url)
        embed.set_thumbnail(url="http://leekwarswiki.net/images/7/70/Poireaux.png")
        await ctx.send(embed=embed)


def get_headers(token):
    return {
        'Authorization': f'Bearer {token}',
        "Cookie": "PHPSESSID=" + str(randint(0, 1000))
    }


def get_farmer(token):
    req = requests.get(f"https://leekwars.com/api/farmer/get-from-token",
                       headers=get_headers(token))
    return req.json()['farmer']


async def run_fights(headers, leek_id, count, farmer_id):
    id_fights = list()
    for _ in range(count):
        response = await arequests.get(
            f"https://leekwars.com/api/garden/get-leek-opponents/{leek_id}",
            headers=headers)

        target = response.json()['opponents'][0]['id']

        response = await arequests.post(
            "https://leekwars.com/api/garden/start-solo-fight",
            data={"leek_id": leek_id,
                  "target_id": target},
            headers=headers)

        id_fights.append(response.json()['fight'])
    await asyncio.sleep(1)
    return format_fight_results(id_fights, farmer_id, headers)


def format_fight_results(id_fights, farmer_id, headers):
    res = {'total': 0, 'win': 0, 'loose': 0, 'tie': 0}
    for id_fight in id_fights:
        fight = get_fight(id_fight, headers)
        win = is_fight_win(fight, farmer_id)
        res['total'] += 1
        if win is not None:
            res['win'] += int(win)
            res['loose'] += int(not win)
        else:
            res['tie'] += 1
    return res


def get_fight(fight_id, headers):
    response = requests.get(
        f"https://leekwars.com/api/fight/get/{fight_id}",
        headers=headers)
    return response.json()


def is_fight_win(fight, farmer_id):
    winner = fight['winner']
    if winner == 0:
        return None
    return (winner == 1 and str(farmer_id) in fight['farmers1'].keys()) \
        or (winner == 2 and (farmer_id) in fight['farmers2'].keys())


def check_dm_channel(message, member):
    return message.author == member and isinstance(message.channel, discord.channel.DMChannel)


def check_good_channel(message, ctx):
    return message.author == ctx.message.author and message.channel == ctx.channel
