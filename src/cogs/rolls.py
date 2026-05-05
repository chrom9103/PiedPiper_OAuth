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
    except Exception as e:
        print(f"Failed to register app commands: {e}")

