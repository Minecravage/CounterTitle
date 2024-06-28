import discord
from discord.ext import commands
import os
import asyncio
import time
import datetime
from discord import app_commands
import sqlite3
from dotenv import load_dotenv

load_dotenv()
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS server(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     discord TEXT,
     mode TEXT,
     titre TEXT
)
""")
conn.commit()

#Bot discord
tokenvar = os.getenv('token')
collection_images = 'https://ibb.co/album/Cs8hnN'
version = '0.0.1'
author = ['Justme']
hexcolor = discord.Color.from_str("#c1e8e3")

bot = commands.Bot(command_prefix='&', intents=discord.Intents.all())
tree = bot.tree
bot.remove_command('help')


#Commandes avec prefix

@bot.command()
async def ping(ctx):

    ping_embed = discord.Embed(
        title="Pong !",
        description='Le bot est en ligne !',
        color=hexcolor,
        timestamp=datetime.datetime.now()
    )
    ping_embed.set_image(url="https://i.ibb.co/n8gnc7T/Ping-embed-image.jpg")
    ping_embed.add_field(name="Version", value=str(version), inline=True)
    ping_embed.add_field(name="Collection image", value=str(collection_images), inline=True)

    await ctx.send(embed=ping_embed)


@bot.command()
async def cns(ctx, *nexttitle: str):

    if ctx.author.guild_permissions.administrator:
        nom_serveur = " ".join(nexttitle)
      
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
                    guild = bot.get_guild(guild_id)
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
            color=hexcolor,
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

@bot.command()
async def mode(ctx, type: str):
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
                    guild = bot.get_guild(guild_id)
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
            else:
                cursor.execute("INSERT INTO server (discord, mode, titre) VALUES (?, ?, ?)", (str(ctx.guild.id), str(type), str(ctx.guild.name)))
                conn.commit()
            await ctx.message.add_reaction("👍")

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

    

@bot.command()
async def help(ctx, commande='not specified'):
    if commande == 'not specified':
        helpembed = discord.Embed(
            title="Panneau d'aide",
            description="Voici les commandes que le bot prends en charge ainsi que leurs utilitées.\nPour rapelle, les arguments entre [] sont obligatoire, tandis que ceux entre <> sont facultatif",
            color=hexcolor,
            timestamp=datetime.datetime.now()
        )
        helpembed.set_image(url="https://i.ibb.co/jJrzsfb/435320e42e3c131e7527924fbd66b68f.gif")
        helpembed.add_field(name="&ping", value="Le bot répond afin de vérifier sa présence en ligne", inline=False)
        helpembed.add_field(name="&cns [nouveau nom de serveur]", value="Change le nom du serveur", inline=False)
        helpembed.add_field(name="&mode", value="Change le mode du compteur de membre présent dans le titre", inline=False)
        helpembed.add_field(name="&help <commande>", value="Affiche le panneau d'aide", inline=False)
        await ctx.send(embed=helpembed)

    elif commande.lower() == 'ping' :
        helpembed = discord.Embed(
            title="Panneau d'aide",
            description="`&ping`\nCette commande vérifie l'état du bot, en indiquant la version, et où trouver la collection d'image qu'il utilise.\n\nPermission requises : Envoyer des messages",
            color=hexcolor,
            timestamp=datetime.datetime.now()
        )
        helpembed.set_image(url="https://i.ibb.co/x3PgqTF/Help-alternative-embed.jpg")
        await ctx.send(embed=helpembed)
    
    elif commande.lower() == 'cns' :
        helpembed = discord.Embed(
            title="Panneau d'aide",
            description="`&cns [nom du serveur]`\nCette commande permet de changer le nom du serveur, en remplacent %membercount% par le nombre d'utilisateur divisé par 1000, puis arrondi par le mode.\n\nPermission requises : Administrateur",
            color=hexcolor,
            timestamp=datetime.datetime.now()
        )
        helpembed.set_image(url="https://i.ibb.co/x3PgqTF/Help-alternative-embed.jpg")
        await ctx.send(embed=helpembed)

    elif commande.lower() == 'mode' :
        helpembed = discord.Embed(
            title="Panneau d'aide",
            description="`&mode [type]`\nCette commande séléctionne le mode d'affichage du nombre de membre\n\n**Usage:**\n\n`&mode 1` = arrondit au millième près\n`&mode 2` = arrondit au centième près\n`&mode 3` = arrondit au dixième près\n`&mode 4` = arrondit a l'unité près\n\nPermission requises : Administrateur",
            color=hexcolor,
            timestamp=datetime.datetime.now()
        )
        helpembed.set_image(url="https://i.ibb.co/x3PgqTF/Help-alternative-embed.jpg")
        await ctx.send(embed=helpembed)

    elif commande.lower() == 'help' :
        helpembed = discord.Embed(
            title="Panneau d'aide",
            description="`&help`\nCette commande permet de vérifier l'usage des autres commandes\n\nPermission requises : Envoyer des messages",
            color=hexcolor,
            timestamp=datetime.datetime.now()
        )
        helpembed.set_image(url="https://i.ibb.co/x3PgqTF/Help-alternative-embed.jpg")
        await ctx.send(embed=helpembed)


#Event

#CMD error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument requis pour cette commande.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Commande inconnue. Veuillez vérifier votre commande.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Un argument fourni est incorrect. Veuillez vérifier et réessayer.")
    else:
        await ctx.send("Une erreur s'est produite lors de l'exécution de la commande.")
        # Log the error for debugging
        print(f"Erreur lors de l'exécution de la commande: {error}")

# On ready
@bot.event
async def on_ready():

    print(f'Logged in as {bot.user} (ID: {bot.user.id})\n\n------')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s).')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="compter vos membres"))

# Join
@bot.event
async def on_member_join(member):
    guild_id = member.guild.id
    discord_id = (str(guild_id),)
    cursor.execute("SELECT * FROM server WHERE discord = ? ", discord_id)
    ligne = cursor.fetchone()

    if ligne:
        mode = ligne[2]
        titre = ligne[3]

        if mode == "1" :
            guild = bot.get_guild(guild_id)
            member_count = guild.member_count
            member_count = int(member_count)
            member_count = member_count / 1000
            print(str(member_count))

            ram_titre = titre.replace("%membercount%", str(member_count))
            await guild.edit(name=ram_titre)

        elif mode == "2":
            guild = bot.get_guild(guild_id)
            member_count = guild.member_count
            member_count = int(member_count)
            member_count = member_count / 1000
            member_count = round(member_count, 2)
            print(str(member_count))

            ram_titre = titre.replace("%membercount%", str(member_count))
            await guild.edit(name=ram_titre)


        elif mode == "3":
            guild = bot.get_guild(guild_id)
            member_count = guild.member_count
            member_count = int(member_count)
            member_count = member_count / 1000
            member_count = round(member_count, 1)
            print(str(member_count))

            ram_titre = titre.replace("%membercount%", str(member_count))
            await guild.edit(name=ram_titre)


        elif mode == "4":
            guild = bot.get_guild(guild_id)
            member_count = guild.member_count
            member_count = int(member_count)
            member_count = member_count / 1000
            member_count = round(member_count, 0)
            print(str(member_count))

            ram_titre = titre.replace("%membercount%", str(member_count))
            await guild.edit(name=ram_titre)

        
    else:
        pass

@bot.event
async def on_member_remove(member):
    guild_id = member.guild.id
    discord_id = (str(guild_id),)
    cursor.execute("SELECT * FROM server WHERE discord = ? ", discord_id)
    ligne = cursor.fetchone()

    if ligne:
        mode = ligne[2]
        titre = ligne[3]

        if mode == "1" :
            guild = bot.get_guild(guild_id)
            member_count = guild.member_count
            member_count = int(member_count)
            member_count = member_count / 1000
            print(str(member_count))

            ram_titre = titre.replace("%membercount%", str(member_count))
            await guild.edit(name=ram_titre)

        elif mode == "2":
            guild = bot.get_guild(guild_id)
            member_count = guild.member_count
            member_count = int(member_count)
            member_count = member_count / 1000
            member_count = round(member_count, 2)
            print(str(member_count))

            ram_titre = titre.replace("%membercount%", str(member_count))
            await guild.edit(name=ram_titre)


        elif mode == "3":
            guild = bot.get_guild(guild_id)
            member_count = guild.member_count
            member_count = int(member_count)
            member_count = member_count / 1000
            member_count = round(member_count, 1)
            print(str(member_count))

            ram_titre = titre.replace("%membercount%", str(member_count))
            await guild.edit(name=ram_titre)


        elif mode == "4":
            guild = bot.get_guild(guild_id)
            member_count = guild.member_count
            member_count = int(member_count)
            member_count = member_count / 1000
            member_count = round(member_count, 0)
            print(str(member_count))

            ram_titre = titre.replace("%membercount%", str(member_count))
            await guild.edit(name=ram_titre)

        
    else:
        pass
    


# Remove bot
@bot.event
async def on_guild_remove(guild):
    discord_id = (str(guild.id),)
    cursor.execute("DELETE FROM server WHERE discord = ?", discord_id)
    conn.commit()



bot.run(tokenvar)