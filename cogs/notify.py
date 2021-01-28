import discord
from Admin.database import Threads
from Admin.admin import Checks
commands = discord.ext.commands

class Notify(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command(aliases=["alert"])
  async def notify(self, ctx, *, member:discord.Member=None):
    if not member:
      member = ctx.author
    channel = ctx.channel
    if not Threads.exists(channel): return
    data = Threads.get(channel)
    if data['subscribed'] == None:
      pass
    elif member.id in data['subscribed']:
      return await ctx.send(embed=discord.Embed(
        description=f"{member.mention} is already being notified for any new messages.",
        color=discord.Color.red()
      ))
    if data['notify'] == None:
      notify = []
    else:
      if member.id in data['notify']: return await ctx.send(embed=discord.Embed(
        description=f"{member.mention} will already be notified on a new message.",
        color=discord.Color.red()
      ))
      notify = data['notify']
    notify.append(member.id)
    Threads.update(channel, {"notify":notify})
    return await ctx.send(embed=discord.Embed(
      description=f"{member.mention} will be notified on a new message.",
      color=discord.Color.green()
    ))


  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command(aliases=["sub", "simp"])
  async def subscribe(self, ctx, *, member:discord.Member=None):
    if not member:
      member = ctx.author
    channel = ctx.channel
    if not Threads.exists(channel): return
    data = Threads.get(channel)
    if data['subscribed'] != None and member.id in data['subscribed']:
      return await ctx.send(embed=discord.Embed(
        description=f"{member.mention} is already being notified for any new messages.",
        color=discord.Color.red()
      ))
    if data['notify'] == None:
      pass
    elif member.id in data['notify']:
      notify = data['notify']
      notify.remove(member.id)
      Threads.update(channel, {"notify":notify})
    subscribed = data['subscribed']
    if subscribed == None:
      subscribed = []
    subscribed.append(member.id)
    Threads.update(channel, {"subscribed":subscribed})
    return await ctx.send(embed=discord.Embed(
      description=f"{member.mention} will now be notified for any new messages.",
      color=discord.Color.green()
    ))

  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command(aliases=["eh", "unsub"])
  async def unsubcribe(self, ctx, *, member:discord.Member=None):
    if not member:
      member = ctx.author
    channel = ctx.channel
    if not Threads.exists(channel): return
    data = Threads.get(channel)
    if data['subscribed'] == None or not member.id in data['subscribed']:
      return await ctx.send(embed=discord.Embed(
        description=f"{member.mention} is not subscribed to this thread.",
        color=discord.Color.red()
      ))
    subs = data['subscribed']
    subs.remove(member.id)
    if len(subs) == 0: subs=None
    Threads.update(channel, {"subscribed":subs})
    return await ctx.send(embed=discord.Embed(
      description=f"{member.mention} will no longer be notified.",
      color=discord.Color.green()
    ))

def setup(bot):
  bot.add_cog(Notify(bot))