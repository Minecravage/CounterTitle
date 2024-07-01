import discord 
import sqlite3
from discord.ext import commands

class On_Member_Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        guild_id = member.guild.id
        discord_id = (str(guild_id),)
        cursor.execute("SELECT * FROM server WHERE discord = ? ", discord_id)
        ligne = cursor.fetchone()

        if ligne:
            mode = ligne[2]
            titre = ligne[3]

            if mode == "1" :
                guild = self.bot.get_guild(guild_id)
                member_count = guild.member_count
                member_count = int(member_count)
                member_count = member_count / 1000
                print(str(member_count))

                ram_titre = titre.replace("%membercount%", str(member_count))
                await guild.edit(name=ram_titre)

            elif mode == "2":
                guild = self.bot.get_guild(guild_id)
                member_count = guild.member_count
                member_count = int(member_count)
                member_count = member_count / 1000
                member_count = round(member_count, 2)
                print(str(member_count))

                ram_titre = titre.replace("%membercount%", str(member_count))
                await guild.edit(name=ram_titre)


            elif mode == "3":
                guild = self.bot.get_guild(guild_id)
                member_count = guild.member_count
                member_count = int(member_count)
                member_count = member_count / 1000
                member_count = round(member_count, 1)
                print(str(member_count))

                ram_titre = titre.replace("%membercount%", str(member_count))
                await guild.edit(name=ram_titre)


            elif mode == "4":
                guild = self.bot.get_guild(guild_id)
                member_count = guild.member_count
                member_count = int(member_count)
                member_count = member_count / 1000
                member_count = round(member_count, 0)
                print(str(member_count))

                ram_titre = titre.replace("%membercount%", str(member_count))
                await guild.edit(name=ram_titre)

            conn.close()

            
        else:
            pass