import discord
from Admin.database import Threads
from core import threads

commands = discord.ext.commands

class DMReply(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot or not isinstance(message.channel, discord.DMChannel): return
    if not Threads.find({"recipient":message.author.id}): return
    channel = self.bot.get_channel(Threads.find({"recipient":message.author.id})["_id"])
    notify = Threads.get(channel)['notify']
    subscribed = Threads.get(channel)['subscribed']
    pings = None
    if notify:
      pings = [self.bot.get_user(i).mention for i in notify]
    if subscribed:
      if not pings:
        pings = [self.bot.get_user(i).mention for i in subscribed]
      else:
        pings += [self.bot.get_user(i).mention for i in subscribed]
    if pings:
      pings = ' '.join(pings)
    mes = await channel.send(content=pings, embed=threads.recipient_embed(message))
    Threads.update(channel, {"notify":None})
    data = Threads.get(channel)
    if data['close'] != None:
      Threads.update(channel, {"close":None})
      await channel.send(embed=discord.Embed(
        description="Close canceled, new message recieved.",
        color=discord.Color.red()
      ))
    return Threads.add_message(channel, message, mes)

def setup(bot):
  bot.add_cog(DMReply(bot))