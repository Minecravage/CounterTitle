import discord 
from discord.ext import commands

class On_Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})\n\n------')
        try:
            synced = await self.bot.tree.sync()
            print(f'Synced {len(synced)} command(s).')
        except Exception as e:
            print(f'Failed to sync commands: {e}')

        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="compter vos membres"))