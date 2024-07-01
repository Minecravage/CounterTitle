import discord 
from discord.ext import commands

class On_Guild_Join(commands.Cog):
    def __init__(self, bot, partnert):
        self.bot = bot
        self.partnertext = partnert

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        owner_id = guild.owner_id
        owner = await self.bot.fetch_user(owner_id)
        await owner.send(self.partnertext)