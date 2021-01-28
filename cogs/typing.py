import discord
from Admin.database import Threads

commands = discord.ext.commands

class TypeSync(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_typing(self, channel, user, when):
    if not isinstance(channel, discord.DMChannel): return
    if not Threads.find({"recipient":user.id}): return
    channel = self.bot.get_channel(Threads.find({"recipient":user.id})['_id'])
    return await channel.trigger_typing()

def setup(bot):
  bot.add_cog(TypeSync(bot))