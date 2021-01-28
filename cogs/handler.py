import discord
from core import embeds

commands = discord.ext.commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=embeds.error(f"Missing `{error.param}` parameter to use this command"))
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckAnyFailure):
            return await ctx.send(embed=embeds.error(f"You are not allowed to do this."))

def setup(bot):
    bot.add_cog(ErrorHandler(bot))