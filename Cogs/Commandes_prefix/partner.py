import discord
from discord.ext import commands

class Partner(commands.Cog):
    
    def __init__(self, bot, partnert):
        self.bot = bot
        self.partnertext = partnert
        
    @commands.command()
    async def partner(self, ctx):
        await ctx.send(self.partnertext)