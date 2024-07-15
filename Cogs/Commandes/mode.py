import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import datetime

class Mode(commands.Cog):
    def __init__(self, bot, hexcolor):
        self.bot = bot
        self.hexcolor = hexcolor

    @commands.hybrid_command(name='mode', description="Défini le mode du compteur")
    @app_commands.describe(type='Le type de compteur')
    @app_commands.choices(type=[
    app_commands.Choice(name="0.001", value="1"),
    app_commands.Choice(name="0.01", value="2"),
    app_commands.Choice(name="0.1", value="3"),
    app_commands.Choice(name="1", value="4")
    ])
    async def mode(self, ctx, type: str):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if ctx.author.guild_permissions.administrator:
            if type in ["1", "2", "3", "4"]:
                discord_id = (str(ctx.guild.id),)
                cursor.execute("SELECT * FROM server WHERE discord = ? ", discord_id)
                ligne = cursor.fetchone()

                if ligne:
                    cursor.execute("UPDATE server SET mode = ? WHERE discord = ?", (str(type), str(ctx.guild.id)))
                    conn.commit()
                    guild_id = ctx.guild.id
                discord_id = (str(guild_id),)
                cursor.execute("SELECT * FROM server WHERE discord = ?", discord_id)
                ligne = cursor.fetchone()
                
                if ligne:
                    mode = ligne[2]
                    titre = ligne[3]

                    if mode in ["1", "2", "3", "4"]:
                        guild = self.bot.get_guild(guild_id)
                        member_count = guild.member_count
                        member_count = int(member_count) / 1000

                        if mode == "1":
                            member_count = member_count  # Ne pas arrondir
                        elif mode == "2":
                            member_count = round(member_count, 2)
                        elif mode == "3":
                            member_count = round(member_count, 1)
                        elif mode == "4":
                            member_count = round(member_count, 0)
                            
                        ram_titre = titre.replace("%membercount%", str(member_count))
                        await ctx.guild.edit(name=ram_titre)
                else:
                    cursor.execute("INSERT INTO server (discord, mode, titre) VALUES (?, ?, ?)", (str(ctx.guild.id), str(type), str(ctx.guild.name)))
                    conn.commit()
                modeembed = discord.Embed(
                title="Succès",
                description=f'La commande à bien été éxécuté',
                color=self.hexcolor,
                timestamp=datetime.datetime.now()
                )
                await ctx.send(embed=modeembed)

            else :
                modeembed = discord.Embed(
                title="Erreur",
                description=f'Vérifie l\'usage de la commande',
                color=discord.Color.from_str("#ff0000"),
                timestamp=datetime.datetime.now()
                )
                await ctx.send(embed=modeembed)
        else:
            modeembed = discord.Embed(
                title="Erreur",
                description=f'Tu n\'as pas les les permissions requises',
                color=discord.Color.from_str("#ff0000"),
                timestamp=datetime.datetime.now()
                )
            await ctx.send(embed=modeembed)

        conn.close()
        