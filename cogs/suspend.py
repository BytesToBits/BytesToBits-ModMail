import discord
from Admin.database import Threads

commands = discord.ext.commands

class Suspend(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def suspend(self, ctx):
    if not Threads.exists(ctx.channel): return
    Threads.delete(ctx.channel)
    return await ctx.send(embed=discord.Embed(
      description="`THREAD SUSPENDED`. This is irreversible. Suspending a thread deletes it from the database and is now treated like a normal channel.\nIn other words, this liberal has been silenced.\n\n||you probably wanted to put it in golden modmails but now u cant because move and transfer no longer works mwahahaha||",
      color=discord.Color.orange()
    )
    .set_image(url="https://i.imgur.com/MhE95qj.png"))

def setup(bot):
  bot.add_cog(Suspend(bot))
