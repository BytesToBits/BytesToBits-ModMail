import discord

from core.database import Threads
from core import embeds, checks

commands = discord.ext.commands

class Notify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @checks.canReply()
    @commands.command(aliases=["alert"])
    async def notify(self, ctx, *, user:discord.User=None):
        if not Threads().exists(_id=ctx.channel.id): return
        if user and not ctx.author.guild_permissions.administrator: return await ctx.send(embed=embeds.Embeds("You are not allowed to do that.").error())
        elif not user: user = ctx.author

        current_notify = Threads().get(_id=ctx.channel.id)["notify"]
        current_subscribed = Threads().get(_id=ctx.channel.id)["subscribed"]

        if not current_subscribed: pass
        elif f"<@{user.id}>" in current_subscribed: return await ctx.send(embed=embeds.Embeds("This user is already being notified for all new messages.").error())

        if not current_notify: current_notify = []
        current_notify.append(f"<@{user.id}>")

        Threads(ctx.channel.id).update_thread(notify=current_notify)

        return await ctx.send(embed=embeds.Embeds(f"{user.mention} will now be notified for a new message.").success())

def setup(bot):
    bot.add_cog(Notify(bot))