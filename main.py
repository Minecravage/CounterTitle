#Imports des libraires
import discord
from discord.ext import commands
import os
import asyncio
import time
import datetime
from discord import app_commands
import sqlite3
from dotenv import load_dotenv

#Import des cogs
from Cogs.Commandes_prefix.ping import Ping
from Cogs.Commandes_prefix.partner import Partner
from Cogs.Commandes_prefix.mode import Mode
from Cogs.Commandes_prefix.help import Help
from Cogs.Commandes_prefix.cns import Cns

from Cogs.Events.on_command_error import On_Command_Error
from Cogs.Events.on_guild_join import On_Guild_Join
from Cogs.Events.on_guild_remove import On_Guild_Remove
from Cogs.Events.on_member_join import On_Member_Join
from Cogs.Events.on_member_remove import On_Member_Remove
from Cogs.Events.on_ready import On_Ready


load_dotenv()

#Variables modifiables
hex = "#c1e8e3"
partner_texte = "# Notre partenaire\nhttps://discord.gg/bqp3bJSMqj\nhttps://linktr.ee/alirex\nMerci de rejoindre, ça nous fait vraiment plaisir !"

# Variables a ne pas toucher
bot = commands.Bot(command_prefix='&', intents=discord.Intents.all())
tree = bot.tree
bot.remove_command('help')
tokenvar = os.getenv('token')
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
conn.close()

    

async def main():

    #Commandes préfixées
    await bot.add_cog(Ping(bot, discord.Color.from_str(hex)))
    await bot.add_cog(Cns(bot, discord.Color.from_str(hex)))
    await bot.add_cog(Help(bot, discord.Color.from_str(hex)))
    await bot.add_cog(Partner(bot, partner_texte))
    await bot.add_cog(Mode(bot))

    #Commandes slash

    #Event
    await bot.add_cog(On_Command_Error(bot))
    await bot.add_cog(On_Guild_Join(bot, partner_texte))
    await bot.add_cog(On_Guild_Remove(bot))
    await bot.add_cog(On_Member_Join(bot))
    await bot.add_cog(On_Member_Remove(bot))
    await bot.add_cog(On_Ready(bot))
    
    await bot.start(tokenvar)


asyncio.run(main())