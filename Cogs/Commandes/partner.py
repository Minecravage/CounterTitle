import discord
from discord.ext import commands
from discord import app_commands

class Partner(commands.Cog):
    
    def __init__(self, bot, partnert):
        self.bot = bot
        self.partnertext = partnert
        
    @commands.hybrid_command(name='partner', description="Affiche les partenaires du bot")
    async def partner(self, ctx):
        await ctx.send(self.partnertext)