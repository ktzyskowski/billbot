import discord
import pytz
import os
from discord import Message, Member
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


def now():
    return datetime.now(tz=pytz.timezone('US/Eastern'))


@bot.command()
async def bill(ctx: Context):
    me = await ctx.guild.fetch_member(498870829095059476)
    async for msg in ctx.channel.history(limit=10_000):
        if msg.author == me and ("https://store.steampowered.com" in msg.content or "http://store.steampowered.com" in msg.content):
            days = (now() - msg.created_at).days
            days_str = "1 day" if days == 1 else f"{days} days"
            await ctx.reply(f"The last time Bill sent a new Steam game recommendation in {msg.channel.mention} was {days_str} ago\n{msg.jump_url}")
            return
    await ctx.reply(f"I can't remember the last time Bill recommended a game :(")

bot.run(os.environ['DISCORD_TOKEN'])