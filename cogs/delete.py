import discord
from Admin.database import Threads
from Admin.admin import Checks
commands = discord.ext.commands

class Delete(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command()
  async def delete(self, ctx, msgid=None):
    channel = ctx.channel
    if not Threads.exists(channel): return

    messages = Threads.get(channel)['messages']
    try:
      if not msgid:
        async for message in channel.history(limit=100):
          if str(message.id) in messages:
            key = str(message.id)
            await message.delete()
            break
        else:
          return await ctx.send(embed=discord.Embed(
            description="Cannot find a message to delete.",
            color=discord.Color.red()
          ))
        async for message in self.bot.get_user(Threads.get(channel)['recipient']).history(limit=100):
          if messages[key] == message.id:
            await message.delete()
            break
        else:
          return await ctx.send(embed=discord.Embed(
            description="Could not find message to delete in recipient's DMs.",
            color=discord.Color.red()
          ))
        return await ctx.message.add_reaction("✅")
      else:
        message = await channel.fetch_message(int(msgid))
        await message.delete()
        async for message in self.bot.get_user(Threads.get(channel)['recipient']).history(limit=100):
          if messages[msgid] == message.id:
            await message.delete()
            break
        else:
          return await ctx.send(embed=discord.Embed(
            description="Could not find message to delete in recipient's DMs.",
            color=discord.Color.red()
          ))
        return await ctx.message.add_reaction("✅")
    except Exception as e:
      return await ctx.send(embed=discord.Embed(
        description=f"```{e}```",
        color=discord.Color.red()
      ))
  

def setup(bot):
  bot.add_cog(Delete(bot))