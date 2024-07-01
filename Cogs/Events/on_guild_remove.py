import discord 
from discord.ext import commands
import sqlite3

class On_Guild_Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        discord_id = (str(guild.id),)
        cursor.execute("DELETE FROM server WHERE discord = ?", discord_id)
        conn.commit()
        conn.close()