import discord
from discord.ext import commands
import datetime
from discord import app_commands

class Ping(commands.Cog):
    def __init__(self, bot, hexcolor):
        self.bot = bot
        self.hexcolor = hexcolor

    @commands.hybrid_command(name='ping', description="Répond pour vérifier la présence du bot")
    async def ping(self, ctx: commands.Context):
        ping_embed = discord.Embed(
        title="Pong !",
        description='Le bot est en ligne !',
        color=self.hexcolor,
        timestamp=datetime.datetime.now()
        )

        ping_embed.set_image(url="https://i.ibb.co/n8gnc7T/Ping-embed-image.jpg")
        ping_embed.add_field(name="Version", value=str("1.0.0"), inline=True)
        ping_embed.add_field(name="Collection image", value=str("https://ibb.co/album/Cs8hnN"), inline=True)

        await ctx.send(embed=ping_embed)

    