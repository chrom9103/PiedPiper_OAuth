import discord
from discord.ext import commands
import random
import json
import os

intents = discord.Intents.all()
intents.message_content = True

# config.jsonの読み込み
with open('.gitignore\config.json') as config_file:
    config = json.load(config_file)
    token = config["token"]  # config.jsonからトークンを取得

bot = commands.Bot(
    command_prefix="?",
    case_insensitive=True,
    intents=intents
)

@bot.event
async def on_ready():
    print("Cleared to take off!")

@bot.command()
async def dice(ctx, m: int, n: int): # mDnを実行
    if ctx.author.bot:
        return

    if m < 1:
        await ctx.reply("1回より多く振ってください")
        return
    if n < 1:
        await ctx.reply("1より大きなダイスにしてください")
        return

    total = 0
    for i in range(m):
        total += random.randint(1, n)
    await ctx.reply(total)

# ボットの実行
bot.run(token)
