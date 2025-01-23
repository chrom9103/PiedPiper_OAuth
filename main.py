import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.message_content = True

load_dotenv('.env')
token = os.getenv("TOKEN")

bot = commands.Bot(
    command_prefix="?",
    case_insensitive=True,
    intents=intents
)

@bot.event
async def on_ready():
    print("Cleared to take off!")

@bot.event
async def on_member_join(member):
    role_name = "member"  # サーバー内で設定したいロール名
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

@bot.command()
async def ping(ctx): # mDnを実行
    if ctx.author.bot:
        return
    await ctx.reply("pong")

# ボットの実行
bot.run(token)
