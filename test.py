import discord
from discord.ext import commands
import json
import random
import string
import time
import os
from datetime import datetime
import aiohttp
import csv
import math
import re

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

#カウントダウンタイマーの関数　countdown_timer(n秒)
def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        time.sleep(1)
    print("The timer was ended.")

@bot.command()
async def dice(ctx,rolls:int,sides:int):
    if ctx.author.bot:
        return

    if rolls < 1 or sides < 1:
        await ctx.reply("ダイスの個数や面数は1以上で指定してください。")
        return

    result = roll_dice(rolls,sides)
    await ctx.reply(result)

def roll_dice(rolls:int,sides:int):
    result:int
    result = 0
    for i in range(rolls):
        result += random.randint(1,sides)
    
    return result

@bot.event
async def on_message(ctx):
    global category,data,message_thread,log_ch
    if ctx.author.bot:
        return

    # メッセージが「int+"d"+int」の形式に一致するかチェック
    pattern = r'^(\d+)d(\d+)$'
    match = re.match(pattern, ctx.content)

    if match:
        rolls = int(match.group(1))
        sides = int(match.group(2))

        if rolls < 1 or sides < 1:
            await ctx.reply("ダイスの個数や面数は1以上で指定してください。")
            return

        result = roll_dice(rolls,sides)

        await ctx.reply(f"{rolls}d{sides} -> {result}")
    

    # メッセージに「{{int+"d"+int}}」の形式が含まれているかチェック
    pattern = r'\{\{(\d+)d(\d+)\}\}'
    matches = re.finditer(pattern, ctx.content)

    new_message_parts = []
    last_end = 0

    for match in matches:
        rolls = int(match.group(1))
        sides = int(match.group(2))

        if rolls < 1 or sides < 1:
            await ctx.reply("ダイスの個数や面数は1以上で指定してください。")
            return

        result = roll_dice(rolls,sides)

        # 変更後のメッセージ
        new_message_parts.append(ctx.content[last_end:match.start()])
        new_message_parts.append(str(result))
        last_end = match.end()

    new_message_parts.append(ctx.content[last_end:])

    new_message = ''.join(new_message_parts)

    # 変更がある場合のみ返信
    if new_message != ctx.content:
        await ctx.reply(new_message)

# 新しいメンバーがサーバーに参加した際のイベント
@bot.event
async def on_member_join(member):
    role_name = "pre-member"  # サーバー内で設定したいロール名
    guild = member.guild

    role = discord.utils.get(guild.roles, name=role_name)
    
    if role is not None:
        try:
            # ロールを付与
            await member.add_roles(role)
            print(f"Role {role_name} has been granted to {member.name}")
        except discord.Forbidden:
            print("Permission error: role cannot be granted.")
        except discord.HTTPException as e:
            print(f"HTTP error: {e}")
    else:
        print(f"Role '{role_name}' was not been found.")

bot.run(token)
