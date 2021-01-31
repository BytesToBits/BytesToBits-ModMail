import discord, re

from core import embeds, checks, database

commands = discord.ext.commands

class ThreadMove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command(aliases=["transfer"])
    async def move(self, ctx, *, catName):
        if not database.Threads().exists(_id=ctx.channel.id): return
        print(1)
        try:
            category = self.bot.get_channel(int(catName))
            await ctx.channel.edit(category=category, overwrites=category.overwrites)
            return await ctx.send(embed=embeds.Embeds(f"Channel moved to `{category.name}`.").success())
        except: pass
        
        catName += ".*"

        for category in ctx.guild.categories:
            if re.fullmatch(catName.lower(), category.name.lower()):
                await ctx.channel.edit(category=category, overwrites=category.overwrites)
                return await ctx.send(embed=embeds.Embeds(f"Channel moved to `{category.name}`.").success())
        else:
            return await ctx.send(embed=embeds.Embeds("Category not found.").error())

def setup(bot):
    bot.add_cog(ThreadMove(bot))