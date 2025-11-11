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

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        member_list_file = os.path.join("datas", "member_list.txt")
        guild = member.guild

        try:
            with open(member_list_file, "r") as file:
                allowed_members = {line.strip() for line in file.readlines()}
                print("allowed members:", allowed_members)

            if str(member.id) in allowed_members:
                # member を付与
                load_dotenv(os.path.join("datas", "main_roleID.env"))
                target_role_id = os.getenv("member")
                if not target_role_id:
                    print("No 'member' role id found in datas/main_roleID.env")
                    return
                role = discord.utils.get(guild.roles, id=int(target_role_id))
                if role is not None:
                    try:
                        await member.add_roles(role)
                        print(f"Role {role.name} has been granted to {member.name}.")
                    except discord.Forbidden:
                        print(f"Permission error: {role.name} role cannot be granted to {member.name}.")
                    except discord.HTTPException as e:
                        print(f"HTTP error: {e}")
                else:
                    print(f"Role with id {target_role_id} was not found in guild {guild.name}.")
            else:
                # pre-member を付与
                load_dotenv(os.path.join("datas", "main_roleID.env"))
                target_role_id = os.getenv("pre-member")
                if not target_role_id:
                    print("No 'pre-member' role id found in datas/main_roleID.env")
                    return
                role = discord.utils.get(guild.roles, id=int(target_role_id))
                if role is not None:
                    try:
                        await member.add_roles(role)
                        print(f"Role {role.name} has been granted to {member.name}")
                    except discord.Forbidden:
                        print("Permission error: role cannot be granted.")
                    except discord.HTTPException as e:
                        print(f"HTTP error: {e}")
                else:
                    print(f"Role with id {target_role_id} was not found in guild {guild.name}.")
        except FileNotFoundError:
            print(f"File '{member_list_file}' not found.")

    async def save_member_list(self):
        load_dotenv(os.path.join("datas", "main_roleID.env"))
        target_role_id = os.getenv("member")

        if not target_role_id:
            print("No 'member' role id found in datas/main_roleID.env")
            return

        # ここは固定のギルドIDが設定されているためそのまま使用
        target_guild_id = 1304058364560543815
        guild = self.bot.get_guild(target_guild_id)
        if guild:
            role = discord.utils.get(guild.roles, id=int(target_role_id))
            if role:
                members_with_role = [member.id for member in guild.members if role in member.roles]
                os.makedirs("datas", exist_ok=True)
                with open(os.path.join("datas", "member_list.txt"), "w") as file:
                    for member_id in members_with_role:
                        file.write(f"{member_id}\n")
                print("Member list saved.")
            else:
                print(f"Role with id {target_role_id} not found in guild {guild.name}.")
        else:
            print(f"Guild with ID {target_guild_id} not found.")

async def setup(bot: commands.Bot):
    # discord.py v2-style async setup for extensions
    await bot.add_cog(RoleManager(bot))
