import discord

from core.database import Logs, Threads
from core import checks

commands = discord.ext.commands

class ModLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @checks.canReply()
    @commands.command()
    async def logs(self, ctx, userID):
        logs = Logs(1).store_logs(userID)
        return await ctx.send(embed=discord.Embed(
            title=f"Logs for UserID: {userID}",
            description='\n'.join([f'https://logs.bytestobits.dev/{i.replace("_", "/")}' for i in logs]),
            color=discord.Color.dark_purple()
        ))
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command()
    async def loglink(self, ctx):
        if not Threads().exists(_id=ctx.channel.id): return
        
        return await ctx.send(embed=discord.Embed(
            description=f"https://logs.bytestobits.dev/logs/{ctx.channel.id}",
            color=discord.Color.dark_purple()
        ))

def setup(bot):
    bot.add_cog(ModLogs(bot))