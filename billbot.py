import discord
import pytz
import os
import json
import requests as re
from bs4 import BeautifulSoup as bs
from discord import Message
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime
from dateutil import parser

from config import user_ids
from repo import Repository

intents = discord.Intents.default()
intents.message_content = True

repo = Repository(dbpath='db.json')
bot = commands.Bot(command_prefix='$', intents=intents)
bot.activity = discord.Activity(
    type=discord.ActivityType.listening,
    name="to $bill et. al.")


def now():
    """Return the current datetime for the EST timezone."""
    return datetime.now(tz=pytz.timezone('US/Eastern'))


@bot.event
async def on_message(msg: Message):

    # check if the message is a recommendation from bill
    #   ... if it is, store it!
    if msg.author.id == user_ids['kevin']:
        if ("http://store.steampowered.com" in msg.content) or\
                ("https://store.steampowered.com" in msg.content):
            repo.put('bill', {
                'created_at': msg.created_at.isoformat(),
                'channel': msg.channel.mention,
                'jump_url': msg.jump_url
            })


@bot.hybrid_command()
async def bill(ctx: Context):
    if not repo.contains('bill'):
        await ctx.reply(f"I can't remember the last time Bill recommended a game :(")
        return

    data = repo.get('bill')
    created_at = parser.parse(data['created_at'])
    channel = data['channel']
    jump_url = data['jump_url']

    days_since = (now() - created_at).days
    days_str = "1 day" if days_since == 1 else f"{days_since} days"
    await ctx.reply(f"The last time Bill sent a new Steam game recommendation in {channel} was {days_str} ago\n{jump_url}")


@bot.hybrid_command()
async def ethan(ctx: Context):
    res = get_ethans_league_ranks()
    if res is None:
        await ctx.reply(f"I can't find Ethan's current League ranks :(")
    else:
        tier, division = res
        await ctx.reply(f"Ethan's current solo/duo rank is {str.capitalize(tier)} {division}")


def get_ethans_league_ranks():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    web_page = re.get(
        "https://www.op.gg/summoners/na/papa%20eef", headers=headers)
    soup = bs(web_page.text, features="html.parser")
    data = json.loads(soup.find(id="__NEXT_DATA__").text)[
        "props"]["pageProps"]["data"]["league_stats"]
    for queue in data:
        if queue["queue_info"]["game_type"] == "SOLORANKED":
            tier = queue["tier_info"]["tier"]
            division = queue["tier_info"]["division"]
            return tier, division
    return None


if __name__ == "__main__":
    bot.run(os.environ['DISCORD_TOKEN'])
