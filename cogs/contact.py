import discord
from Admin.database import Threads
from Admin.admin import Files, Checks

commands = discord.ext.commands

class Contact(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command(aliases=["newthread"])
  async def contact(self, ctx, *, user:discord.User=None):
    if not user:
      return await ctx.send(embed=discord.Embed(
        description="You must enter a user to contact.",
        color=discord.Color.red()
      ))
    channel = await self.bot.get_channel(Files.get("support")["categories"]["general"]["id"]).create_text_channel(name=f"{user.name}-{user.discriminator}", topic=f"User ID: {user.id}")
    Threads.raw_add({
      "_id":channel.id,
      "recipient":user.id,
      "channel":None,
      "close":None,
      "notify":None,
      "subscribed":None,
      "messages":{}
    })
    await channel.send(embed=discord.Embed(
      description=f"Thread for {user.mention} started by {ctx.author.mention}",
      color=discord.Color.purple()
    ))
    return await ctx.send(embed=discord.Embed(
      description=f"Started thread for {user.mention} ({channel.mention})",
      color=discord.Color.green()
    ))

def setup(bot):
  bot.add_cog(Contact(bot))