import discord, asyncio
from core.files import Data
from core import database, embeds

from discord.ext import commands

class Close(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def close(self, ctx):
        if (database.Threads().exists(chanelid=ctx.channel.id) != None):
            database.Threads(thread=ctx.channel.id).delete
            await ctx.send('worked')
        else:
            await ctx.send(database.Threads().exists(chanelid=ctx.channel.id) != None == True)


def setup(bot):
    bot.add_cog(Close(bot))
