import discord
from Admin.database import Threads, Snippets
from core import threads
from Admin.admin import Files, Checks

commands = discord.ext.commands

class ModReply(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command(aliases=["r"])
  async def reply(self, ctx, *, message):
    channel = ctx.channel
    if not Threads.exists(channel): return
    recipient = self.bot.get_user(Threads.get(channel)["recipient"])
    try:
      msg = await recipient.send(embed=threads.mod_embed(ctx.message, message)[0])
    except Exception as e:
      print(e)
      return await ctx.send(embed=discord.Embed(
        description="Cannot send messages to this user.",
        color=discord.Color.red()
      ))
    mes = await ctx.send(embed=threads.mod_embed(ctx.message, message)[1])
    Threads.add_message(channel, msg, mes)
    return await ctx.message.delete()
  
  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command(aliases=["ar"])
  async def anonreply(self, ctx, *, message):
    channel = ctx.channel
    if not Threads.exists(channel): return
    recipient = self.bot.get_user(Threads.get(channel)["recipient"])
    try:
      msg = await recipient.send(embed=threads.mod_embed(ctx.message, message, anonymous=True)[0])
    except Exception as e:
      print(e)
      return await ctx.send(embed=discord.Embed(
        description="Cannot send messages to this user.",
        color=discord.Color.red()
      ))
    mes = await ctx.send(embed=threads.mod_embed(ctx.message, message, anonymous=True)[1])
    Threads.add_message(channel, msg, mes)
    return await ctx.message.delete()

  @commands.Cog.listener()
  async def on_message(self, message):
    channel = message.channel
    if not Threads.exists(channel): return
    if not message.content.startswith(Files.config("main", "prefix")*2): return

    snippets = [i["_id"] for i in Snippets.get_all()]

    #Anonymous Snippet
    if message.content.startswith(Files.config("main", "prefix")*3):
      msg = message.content.split(" ")
      name = msg[0][3:]

      if not name.lower() in snippets:
        return await channel.send(embed=discord.Embed(
          description="This snippet does not exist.",
          color=discord.Color.red()
        ))
      try:
        member = self.bot.get_user(Threads.get(channel)['recipient'])
        await member.send(embed=threads.mod_embed(message, Snippets.get(name)["content"], anonymous=True)[0])
        await channel.send(embed=threads.mod_embed(message, Snippets.get(name)["content"], anonymous=True)[1])
        return await message.delete()
      except Exception as e:
        return await channel.send(embed=discord.Embed(
          description=f"```{e}```",
          color=discord.Color.red()
        ))

    #Regular Snippet
    msg = message.content.split(" ")
    name = msg[0][2:]
    if not name.lower() in snippets:
      return await channel.send(embed=discord.Embed(
        description="This snippet does not exist.",
        color=discord.Color.red()
      ))
    try:
      member = self.bot.get_user(Threads.get(channel)['recipient'])
      await member.send(embed=threads.mod_embed(message, Snippets.get(name)["content"], anonymous=False)[0])
      await channel.send(embed=threads.mod_embed(message, Snippets.get(name)["content"], anonymous=False)[1])
      return await message.delete()
    except Exception as e:
      return await channel.send(embed=discord.Embed(
        description=f"```{e}```",
        color=discord.Color.red()
      ))
def setup(bot):
  bot.add_cog(ModReply(bot))