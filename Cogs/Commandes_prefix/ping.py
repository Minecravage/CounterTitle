import discord
from discord.ext import commands
import datetime

class Ping(commands.Cog):
    def __init__(self, bot, hexcolor):
        self.bot = bot
        self.hexcolor = hexcolor

    @commands.command()
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

    