import discord

from core.database import Threads
from core import embeds, checks

commands = discord.ext.commands

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @checks.canReply()
    @commands.command(aliaes=["sub", "simp"])
    async def subscribe(self, ctx, *, user:discord.User=None):
        if not Threads().exists(_id=ctx.channel.id): return
        if user and not ctx.author.guild_permissions.administrator: return await ctx.send(embed=embeds.Embeds("You are not allowed to do that.").error())
        elif not user: user = ctx.author

        current_subscriptions = Threads().get(_id=ctx.channel.id)["subscribed"]

        if not current_subscriptions: current_subscriptions = []
        current_subscriptions.append(f"<@{user.id}>")

        Threads(ctx.channel.id).update_thread(subscribed=current_subscriptions)

        return await ctx.send(embed=embeds.Embeds(f"{user.mention} will now be notified of any new messages.").success())
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command(aliases=["unsub", "eh"])
    async def unsubscribe(self, ctx, *, user:discord.User=None):
        if not Threads().exists(_id=ctx.channel.id): return
        if user and not ctx.author.guild_permissions.administrator: return await ctx.send(embed=embeds.Embeds("You are not allowed to do that.").error())
        elif not user: user = ctx.author

        current_subscriptions = Threads().get(_id=ctx.channel.id)["subscribed"]

        if not current_subscriptions: current_subscriptions = []
        try:
            current_subscriptions.remove(f"<@{user.id}>")
        except:
            return await ctx.send(embed=embeds.Embeds("This user is not subscribed.").error())

        Threads(ctx.channel.id).update_thread(subscribed=current_subscriptions)

        return await ctx.send(embed=embeds.Embeds(f"{user.mention} will no longer be notified of any new messages.").success())

def setup(bot):
    bot.add_cog(Subscribe(bot))