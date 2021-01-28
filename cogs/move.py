import discord, re
from Admin.database import Threads
from Admin.admin import Files, Checks

commands = discord.ext.commands

class Move(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command()
  async def move(self, ctx, *, category=None):
    channel = ctx.channel
    if not Threads.exists(channel): return
    categories = Files.get("support")["categories"]
    names = ', '.join([categories[i]['name'] for i in categories])
    if not category:
      return await ctx.send(embed=discord.Embed(
        title="Available Categories",
        description=names,
        color=discord.Color.blurple()
      ))
    if not category.lower() in [categories[i]['name'].lower() for i in categories]:
      return await ctx.send(embed=discord.Embed(
        description="Category not found.",
        color=discord.Color.red()
      ))
    _id = next(categories[i]['id'] for i in categories if categories[i]['name'].lower() == category.lower())
    categorychannel = self.bot.get_channel(_id)
    await channel.edit(category=categorychannel, overwrites=categorychannel.overwrites)
    return await ctx.send(embed=discord.Embed(
      description=f"Thread moved to `{category.upper()}`.",
      color=discord.Color.green()
    ))

  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command()
  async def transfer(self, ctx, *, category):
    channel = ctx.channel
    if not Threads.exists(channel): return
    for i in ctx.guild.categories:
      if re.match(category, i.name.lower()) or str(i.id) == category:
        await channel.edit(category=i, overwrites=i.overwrites)
        return await ctx.send(embed=discord.Embed(
          description=f"Transferred thread to `{i.name.upper()}`.",
          color=discord.Color.green()
        ))
    return await ctx.send(embed=discord.Embed(
      description="Cannot find category.",
      color=discord.Color.red()
    ))
      
    

def setup(bot):
  bot.add_cog(Move(bot))
      