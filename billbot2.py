import discord
import pytz
import os
import json
import requests as re
from bs4 import BeautifulSoup as bs
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
bot.activity = discord.Activity(
    type=discord.ActivityType.listening, name="Checking the last time $bill sent a new game")


def now():
    return datetime.now(tz=pytz.timezone('US/Eastern'))


@bot.hybrid_command()
async def bill(ctx: Context):
    # kevin: 498870829095059476
    # bill: 99631940310663168
    bill = await ctx.guild.fetch_member(99631940310663168)
    async for msg in ctx.channel.history(limit=10_000):
        if msg.author == bill and ("https://store.steampowered.com" in msg.content or "http://store.steampowered.com" in msg.content):
            days = (now() - msg.created_at).days
            days_str = "1 day" if days == 1 else f"{days} days"
            await ctx.reply(f"The last time Bill sent a new Steam game recommendation in {msg.channel.mention} was {days_str} ago\n{msg.jump_url}")
            return
    await ctx.reply(f"I can't remember the last time Bill recommended a game :(")


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
