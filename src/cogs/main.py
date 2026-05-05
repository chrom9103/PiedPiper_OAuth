import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


class RoleManager(commands.Cog):
    """Cog to manage member roles and member list persistence."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Called when the bot is ready. Save the member list for configured guild.
        print("Cleared to take off!")
        await self.save_member_list()

async def setup(bot: commands.Bot):
    # discord.py v2-style async setup for extensions
    await bot.add_cog(RoleManager(bot))
