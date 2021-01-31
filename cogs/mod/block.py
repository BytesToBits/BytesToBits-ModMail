import discord

from core import database, embeds

from typing import Union

commands = discord.ext.commands

class Blocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def block(self, ctx, user:Union[discord.User, int]=None, reason="No reason specified"):
        if not user:
            if database.Threads().exists(_id=ctx.channel.id):
                userID = database.Threads().get(_id=ctx.channel.id)["recipient"]
                if database.Blocks(userID).blocked: return await ctx.send(embed=embeds.Embeds("This user is already blocked.").error())
                database.Blocks(userID).block(reason=reason)
                return await ctx.send(embed=embeds.Embeds(f"<@{userID}> was successfully blocked.").success())
            else: return

        if isinstance(user, discord.User):
            Block = database.Blocks(user.id)
            if Block.blocked: return await ctx.send(embed=embeds.Embeds("This user is already blocked.").error())
            Block.block(reason=reason)
            return await ctx.send(embed=embeds.Embeds(f"{user.mention} was successfully blocked.").success())
        
        if len(str(user)) == 18:
            Block = database.Blocks(user)
            if Block.blocked: return await ctx.send(embed=embeds.Embeds("This user is already blocked.").error())
            Block.block(reason=reason)
            return await ctx.send(embed=embeds.Embeds(f"<@{user}> was successfully blocked.").success())
            
        else:
            return await ctx.send(embed=embeds.Embeds("Invalid User ID.").error())

    @commands.command()
    async def unblock(self, ctx, user:Union[discord.User, int]=None):
        if not user:
            if database.Threads().exists(_id=ctx.channel.id):
                userID = database.Threads().get(_id=ctx.channel.id)["recipient"]
                if not database.Blocks(userID).blocked: return await ctx.send(embed=embeds.Embeds("This user is not blocked.").error())
                database.Blocks(userID).unblock
                return await ctx.send(embed=embeds.Embeds(f"<@{userID}> was successfully unblocked.").success())
            else: return

        if isinstance(user, discord.User):
            Block = database.Blocks(user.id)
            if not Block.blocked: return await ctx.send(embed=embeds.Embeds("This user is not blocked.").error())
            Block.unblock
            return await ctx.send(embed=embeds.Embeds(f"{user.mention} was successfully unblocked.").success())
        
        if len(str(user)) == 18:
            Block = database.Blocks(user)
            if not Block.blocked: return await ctx.send(embed=embeds.Embeds("This user is not blocked.").error())
            Block.unblock
            return await ctx.send(embed=embeds.Embeds(f"<@{user}> was successfully unblocked.").success())
            
        else:
            return await ctx.send(embed=embeds.Embeds("Invalid User ID.").error())
        
def setup(bot):
    bot.add_cog(Blocks(bot))