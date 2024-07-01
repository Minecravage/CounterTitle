import discord 
from discord.ext import commands

class On_Command_Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
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
            print(f"Erreur lors de l'exécution de la commande: {error}")