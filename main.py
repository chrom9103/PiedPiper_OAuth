import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

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
    await save_member_list()

@bot.event
async def on_member_join(member):
    member_list_file = "datas/member_list.txt"
    guild = member.guild

    try:
        with open(member_list_file, "r") as file:
            allowed_members = [line.strip() for line in file.readlines()]
            print(allowed_members)
            
        if str(member.id) in allowed_members:
            print(str(member.id))
            #memberを付与
            role_name = "member"
            role = discord.utils.get(guild.roles, name=role_name)
            if role is not None:
                try:
                    await member.add_roles(role)
                    print(f"Role {role_name} has been granted to {member.name}.")
                except discord.Forbidden:
                    print(f"Permission error: {role_name} role cannot be granted to {member.name}.")
                except discord.HTTPException as e:
                    print(f"HTTP error: {e}")
            else:
                print(f"Role '{role_name}' was not found in guild {member.guild.name}.")
        else:
            #pre-memberを付与
            role_name = "pre-member"
            role = discord.utils.get(guild.roles, name=role_name)
            if role is not None:
                try:
                    await member.add_roles(role)
                    print(f"Role {role_name} has been granted to {member.name}")
                except discord.Forbidden:
                    print("Permission error: role cannot be granted.")
                except discord.HTTPException as e:
                    print(f"HTTP error: {e}")
            else:
                print(f"Role '{role_name}' was not been found.")
    except FileNotFoundError:
        print(f"File '{member_list_file}' not found.") 

async def save_member_list():
    target_guild_id = 1304058364560543815
    target_role_name = "member"
    member_list_file = "member_list.txt"

    guild = bot.get_guild(target_guild_id)
    if guild:
        role = discord.utils.get(guild.roles, name=target_role_name)
        if role:
            members_with_role = [member.id for member in guild.members if role in member.roles]
            with open("datas/member_list.txt", "w") as file:
                for member in members_with_role:
                    file.write(f"{member}\n")
            print(f"Member list saved to '{member_list_file}'.")
        else:
            print(f"Role '{target_role_name}' not found in guild.")
    else:
        print(f"Guild with ID {target_guild_id} not found.")

@bot.command()
async def ping(ctx):
    if ctx.author.bot:
        return
    file = os.path.basename(__file__)
    await ctx.reply(f"pong [{file}]")

bot.run(token)