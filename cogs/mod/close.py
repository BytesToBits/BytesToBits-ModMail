import discord, datetime

from discord.ext import tasks

from dateparser import parse
from core import database, embeds, checks
from core.files import Data

commands = discord.ext.commands

class ModClose(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.close_threads.start()

    @tasks.loop(seconds=1, reconnect=True)
    async def close_threads(self):
        await self.bot.wait_until_ready()
        threads = database.Threads().get_all()

        closeMessage = Data("closeMessage").read()

        for thread in threads:
            if not thread["close"]: pass
            elif thread["close"] <= datetime.datetime.now():
                try:
                    await self.bot.get_channel(thread["_id"]).delete()
                    await self.bot.get_user(thread["recipient"]).send(embed=discord.Embed(
                        title="Thread Closed",
                        description=closeMessage,
                        color=discord.Color.red(),
                        timestamp=datetime.datetime.utcnow()
                    )
                    .set_footer(text="Thank you for contacting us!"))
                except:
                    pass
                database.Threads(thread["_id"]).delete

    def format_time(self, seconds):
        days, hours, minutes, seconds = seconds//86400, (seconds%86400)//3600, ((seconds%86400)%3600)//60, ((seconds%86400)%3600)%60

        if days == 0:
            if hours == 0:
                if minutes == 0:
                    if seconds == 0:
                        return "Now"
                    else:
                        return f"in {seconds} seconds"
                else:
                    if seconds == 0:
                        return f"in {minutes} minutes"
                    else:
                        return f"in {minutes} minutes and {seconds} seconds"
            else:
                if minutes == 0 and seconds == 0:
                    return f"in {hours} hours"
                elif minutes != 0 and seconds == 0:
                    return f"in {hours} hours and {minutes} minutes"
                elif minutes == 0 and seconds != 0:
                    return f"in {hours} hours and {seconds} seconds"
                else:
                    return f"in {hours} hours, {minutes} minutes and {seconds} seconds"
        else:
            if hours == 0 and minutes == 0 and seconds == 0:
                return f"in {days} days"
            elif hours !=0 and minutes == 0 and seconds == 0:
                return f"in {days} days and {hours} hours"
            elif hours != 0 and minutes != 0 and seconds == 0:
                return f"in {days} days, {hours} hours and {minutes} minutes"
            elif hours != 0 and minutes == 0 and seconds !=0:
                return f"in {days} days, {hours} hours and {seconds} seconds"
            elif hours == 0 and minutes != 0 and seconds != 0:
                return f"in {days} days, {minutes} minutes and {seconds} seconds"
            else:
                return f"in {days} days, {hours} hours, {minutes} minutes and {seconds} seconds"

    @commands.guild_only()
    @checks.canReply()
    @commands.command()
    async def close(self, ctx, *, time="now"):
        thread = database.Threads(ctx.channel.id)
        if not thread.exists(_id=ctx.channel.id): return

        if time.lower() == "cancel":
            thread.update_thread(close=None)
            return await ctx.send(embed=embeds.Embeds(f"Close canceled.").warn())

        closeDate = parse(f"in {time}")
        if closeDate < datetime.datetime.now() and not time == "now": return await ctx.send(embed=embeds.Embeds("Invalid time.").error())

        thread.update_thread(close=closeDate)

        return await ctx.send(embed=embeds.Embeds(f"This thread will close {self.format_time((closeDate-datetime.datetime.now()).seconds)}.").warn())

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if not database.Threads().exists(_id=channel.id): return

        database.Threads(channel.id).delete

def setup(bot):
    bot.add_cog(ModClose(bot))