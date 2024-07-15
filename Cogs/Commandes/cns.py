import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import datetime

class Cns(commands.Cog):
    def __init__(self, bot, hexcolor):
        self.bot = bot
        self.hexcolor = hexcolor

    @commands.hybrid_command(name='cns', description="Changer le nom du serveur")
    @app_commands.describe(nexttitle='Le nouveau nom de votre serveur')
    async def cns(self, ctx, nexttitle: str):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if ctx.author.guild_permissions.administrator:
            nom_serveur = nexttitle

            try :
                discord_id = (str(ctx.guild.id),)
                cursor.execute("SELECT * FROM server WHERE discord = ? ", discord_id)
                ligne = cursor.fetchone()

                if ligne:
                    cursor.execute("UPDATE server SET titre = ? WHERE discord = ?", (nom_serveur, str(ctx.guild.id)))
                    conn.commit()
                else:
                    cursor.execute("INSERT INTO server (discord, mode, titre) VALUES (?, ?, ?)", (str(ctx.guild.id), "1", nom_serveur))
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

                        print(str(member_count))
                        ram_titre = titre.replace("%membercount%", str(member_count))
                        await ctx.guild.edit(name=ram_titre)
                    

                servembed = discord.Embed(
                title="Changement du nom de serveur",
                description=f'Le nom du serveur a été changé pour `{nom_serveur}`',
                color=self.hexcolor,
                timestamp=datetime.datetime.now()
                )
                servembed.set_image(url="https://i.ibb.co/jJrzsfb/435320e42e3c131e7527924fbd66b68f.gif")

                await ctx.send(embed=servembed)
            
            except discord.Forbidden:


                servembed = discord.Embed(
                title="Erreur",
                description='Je n\'ai pas les les permissions requises',
                color=discord.Color.from_str("#ff0000"),
                timestamp=datetime.datetime.now()
                )
                await ctx.send(embed=servembed)
            
            except discord.HTTPException:


                servembed = discord.Embed(
                title="Erreur",
                description=f'Une erreur s\'est produite de manière innatendue',
                color=discord.Color.from_str("#ff0000"),
                timestamp=datetime.datetime.now()
                )
                await ctx.send(embed=servembed)
        else:
            servembed = discord.Embed(
                title="Erreur",
                description=f'Tu n\'as pas les les permissions requises',
                color=discord.Color.from_str("#ff0000"),
                timestamp=datetime.datetime.now()
                )
            await ctx.send(embed=servembed)

        conn.close()