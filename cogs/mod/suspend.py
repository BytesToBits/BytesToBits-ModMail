import discord

from core.database import Threads
from core import checks

commands = discord.ext.commands

class Suspend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command()
    async def suspend(self, ctx):
        if not Threads().exists(_id=ctx.channel.id) or not ctx.author.guild_permissions.administrator: return

        Threads(ctx.channel.id).delete

        return await ctx.send(embed=discord.Embed(
            title="Thread Suspended",
            description="This thread is now suspended, meaning it won't be treated as a thread anymore, how cool is that!?",
            color=discord.Color.orange()
        ))
    
def setup(bot):
    bot.add_cog(Suspend(bot))