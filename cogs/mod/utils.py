import discord

from core import checks, database

commands = discord.ext.commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command(name="id")
    async def _id(self, ctx):
        if not database.Threads(ctx.channel.id).exists(_id=ctx.channel.id): return

        return await ctx.send(str(database.Threads(ctx.channel.id).data()['recipient']))

def setup(bot):
    bot.add_cog(Utils(bot))