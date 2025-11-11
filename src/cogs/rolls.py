import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')
load_dotenv(os.path.join('datas', 'main_roleID.env'))


def _get_int_env(name: str):
    val = os.getenv(name)
    try:
        return int(val) if val is not None else None
    except (TypeError, ValueError):
        return None


@app_commands.command(name="mkivt", description="Create an invite link")
async def mkivt(interaction: discord.Interaction):
    if interaction.user.bot:
        return

    if interaction.channel.id != 1342861713300521051:
        await interaction.response.send_message("You cannot use this command in this channel.", ephemeral=True)
        return

    invite = await interaction.channel.create_invite(max_uses=1, max_age=60 * 60 * 24 * 7, reason=f"By {interaction.user.name}")
    await interaction.response.send_message(f"New invite link: {invite.url}")
    await interaction.followup.send(f"Invite ID:`{invite.id}` was created by {interaction.user.name}")

    os.makedirs('datas', exist_ok=True)
    with open(os.path.join("datas", "invite_list.txt"), "a") as log_file:
        log_file.write(f"Invite ID: {invite.id}. Author: {interaction.user.name}\n")


@app_commands.command(name="add", description="Add a role to one member")
@app_commands.describe(role="The role to assign", member="The member to assign the role to")
async def add(interaction: discord.Interaction, role: str, member: discord.Member):
    if interaction.user.bot:
        return

    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
        return

    admin_role_id = _get_int_env("administrator")
    mentor_role_id = _get_int_env("mentor")
    admin_role = discord.utils.get(guild.roles, id=admin_role_id) if admin_role_id else None
    mentor_role = discord.utils.get(guild.roles, id=mentor_role_id) if mentor_role_id else None

    seminar_list = [
        _get_int_env("Unity"),
        _get_int_env("web創作"),
        _get_int_env("課題解決"),
        _get_int_env("機会学習"),
        _get_int_env("discod-bot"),
    ]
    seminar_list = [s for s in seminar_list if s is not None]

    target_role = discord.utils.get(guild.roles, name=role)

    if interaction.channel.id != 1342861713300521051:
        await interaction.response.send_message("You cannot use this command in this channel.", ephemeral=True)
        return

    try:
        # Ensure target_role exists
        if target_role is None:
            await interaction.response.send_message(f"Role named '{role}' was not found.", ephemeral=True)
            return

        user_member = interaction.user

        if role == "member":
            if admin_role is None or admin_role not in getattr(user_member, 'roles', []):
                await interaction.response.send_message("Permission error", ephemeral=True)
                return

            premember_role = discord.utils.get(guild.roles, name="pre-member")
            await member.add_roles(target_role)
            if premember_role:
                await member.remove_roles(premember_role)
            os.makedirs('datas', exist_ok=True)
            with open(os.path.join("datas", "member_list.txt"), "a") as log_file:
                log_file.write(f"{member}\n")
            with open(os.path.join("datas", "member_add_log.txt"), "a") as log_file:
                log_file.write(f"{member.name} by {interaction.user.name}\n")
            print(f"Added {member.name} to {target_role.name}.")

        elif target_role.id in seminar_list:
            if (admin_role is None or admin_role not in getattr(user_member, 'roles', [])) and (mentor_role is None or mentor_role not in getattr(user_member, 'roles', [])):
                await interaction.response.send_message("Permission error", ephemeral=True)
                return

            await member.add_roles(target_role)
            print(f"Added {member.name} to {target_role.name}.")

        await interaction.response.send_message(f"{member.mention} was added to `{target_role.name}`.")

    except discord.Forbidden:
        await interaction.response.send_message("Permission error", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)


class RollsCog(commands.Cog):
    """Cog wrapping the classic commands and lifecycle logic for rolls."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Sync tree when bot is ready
        print(f"Logged in as {self.bot.user.name}")
        try:
            synced = await self.bot.tree.sync()
            print(f"Synced {len(synced)} command(s).")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

async def setup(bot: commands.Bot):
    # Register cog and app commands
    await bot.add_cog(RollsCog(bot))

    # Add app commands defined at module level if not already present
    try:
        if not bot.tree.get_command('mkivt'):
            bot.tree.add_command(mkivt)
        if not bot.tree.get_command('add'):
            bot.tree.add_command(add)
    except Exception as e:
        print(f"Failed to register app commands: {e}")

