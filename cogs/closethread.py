import discord, datetime
from Admin.admin import Files, Checks
from Admin.database import Threads
from dateparser import parse
from discord.ext import tasks

commands = discord.ext.commands

class CloseThread(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.close_check.start()

  def get_close_message(self, ctx, seconds, minutes, hours):
    if not hours and not minutes:
      embed = discord.Embed(
        description=f"This thread will close in {seconds} seconds.",
        color=discord.Color.red()
      )
    elif minutes and not hours:
      embed = discord.Embed(
        description=f"This thread will close in {minutes} minutes and {seconds} seconds.",
        color=discord.Color.red())
    elif minutes and hours:
      embed = discord.Embed(
        description=f"This thread will close in {hours} hours, {minutes} minutes, and {seconds} seconds.",
        color=discord.Color.red()
      )
    else:
      embed = discord.Embed(
        description=f"This thread will close in {hours} hours and {seconds} seconds.",
        color=discord.Color.red()
      )
    embed.set_footer(text=f"Scheduled close by {ctx.author}", icon_url=ctx.author.avatar_url_as(static_format="png"))
    return embed

  @tasks.loop(seconds=1)
  async def close_check(self):
    threads = [i for i in Threads.get_all() if i['close'] != None]
    for i in threads:
      if i['close'] <= datetime.datetime.now():
        try:
          await self.bot.get_user(i['recipient']).send(embed=self.recipient_close_message())
        except:
          pass
        channel = self.bot.get_channel(i['_id'])
        Threads.delete(channel)
        await channel.delete()
  
  def recipient_close_message(self):
    return discord.Embed(
      title="Thanks for contacting Support!",
      description='\n'.join(Files.get("support")["thread_close_message"]),
      color=discord.Color.red()
    )

  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command()
  async def close(self, ctx, *, after="1s"):
    if not Threads.exists(ctx.channel): return
    if after.lower() == "cancel":
      Threads.update(ctx.channel, {"close":None})
      return await ctx.send(embed=discord.Embed(
        description="Close canceled.",
        color=discord.Color.red()
      ))
    try:
      hours = None
      minutes = None
      time = (parse(f"in {after}")-datetime.datetime.now()).seconds+1
      if time > 60:
        if time > 3600:
          hours = time//3600
          time %= 3600
        minutes = time//60
        time%=60
      Threads.update(ctx.channel, {"close":parse(f"in {after}")})
      return await ctx.send(embed=self.get_close_message(ctx, time, minutes, hours))
    except AttributeError:
      return await ctx.send(embed=discord.Embed(
        description="Invalid time entered. Example: `!close 5m`",
        color=discord.Color.orange()
      ))

  @commands.Cog.listener()
  async def on_guild_channel_delete(self, channel):
    if not Threads.exists(channel): return
    Threads.delete(channel)
      


def setup(bot):
  bot.add_cog(CloseThread(bot))