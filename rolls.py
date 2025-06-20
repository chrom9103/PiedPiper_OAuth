import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv('.env')
load_dotenv('./datas/main_roleID.env')
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="?",
    case_insensitive=True,
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="mkivt", description="Create an invite link")
async def mkivt(ctx: discord.Interaction):
    if ctx.user.bot:
        return

    if ctx.channel.id != 1342861713300521051:
        await ctx.response.send_message("You cannot use this command in this channel.", ephemeral=True)
        return

    invite = await ctx.channel.create_invite(max_uses=1, max_age=60*60*24*7, reason=f"By {ctx.user.name}")
    await ctx.response.send_message(f"New invite link: {invite.url}")
    await ctx.followup.send(f"Invite ID:`{invite.id}` was created by {ctx.user.name}")

    with open("datas/invite_list.txt", "a") as log_file:
        log_file.write(f"Invite ID: {invite.id}. Author: {ctx.user.name}\n")


@bot.tree.command(name="add", description="Add a role to one member")
@app_commands.describe(role="The role to assign", member="The member to assign the role to")
async def add(ctx: discord.Interaction,role: str,member: discord.Member):
    if ctx.user.bot:
        return

    admin_role_id = int(os.getenv("administrator"))
    mentor_role_id = int(os.getenv("mentor"))
    admin_role = discord.utils.get(ctx.guild.roles, id=admin_role_id)
    mentor_role = discord.utils.get(ctx.guild.roles, id=mentor_role_id)

    seminar_list = [
        int(os.getenv("Unity")),
        int(os.getenv("web創作")),
        int(os.getenv("課題解決")),
        int(os.getenv("機会学習")),
        int(os.getenv("discod-bot"))
    ]

    target_role = discord.utils.get(ctx.guild.roles, name=role)

    if ctx.channel.id != 1342861713300521051:
        await ctx.response.send_message("You cannot use this command in this channel.", ephemeral=True)
        return

    try:
        if role == "member":
            if admin_role not in ctx.user.roles:
                await ctx.response.send_message("Permission error", ephemeral=True)
                return

            premember_role = discord.utils.get(ctx.guild.roles, name="pre-member")
            await member.add_roles(target_role)
            await member.remove_roles(premember_role)
            with open("datas/member_list.txt", "a") as log_file:
                log_file.write(f"{member}\n")
            with open("datas/member_add_log.txt", "a") as log_file:
                log_file.write(f"{member.name} by {ctx.user.name}\n")
            print(f"Added {member.name} to {target_role.name}.")

        elif target_role and target_role.id in seminar_list:
            if admin_role not in ctx.user.roles and mentor_role not in ctx.user.roles:
                await ctx.response.send_message("Permission error", ephemeral=True)
                return

            await member.add_roles(target_role)
            print(f"Added {member.name} to {target_role.name}.")

        await ctx.response.send_message(f"{member.mention} was added to `{target_role.name}`.")

    except discord.Forbidden:
        await ctx.response.send_message("Permission error", ephemeral=True)
    except discord.HTTPException as e:
        await ctx.response.send_message(f"An error occurred: {e}", ephemeral=True)

@bot.command()
async def ping(ctx):
    if ctx.author.bot:
        return
    file = os.path.basename(__file__)
    await ctx.reply(f"pong [{file}]")

bot.run(token)
