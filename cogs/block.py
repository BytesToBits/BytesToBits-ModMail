import discord
from typing import Union
from Admin.admin import Checks
from Admin.database import Blocks

commands = discord.ext.commands

class Block(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.guild_only()
  @Checks.reply()
  @commands.command()
  async def block(self, ctx, user:Union[discord.User, int]=None, *, reason="No reason specified."):
    if not user: return await ctx.send(embed=discord.Embed(
      description="You must specify a user to block.",
      color=discord.Color.red()
    ))
    if isinstance(user, int):
      try:
        user = self.bot.get_user(user)
        user.id
      except Exception as e:
        print(e)
        return await ctx.send(embed=discord.Embed(
          description="You must specify a user to block.",
          color=discord.Color.red()
        ))
    if Blocks.exists(user): return await ctx.send(embed=discord.Embed(
      description="This user is already blocked.",
      color=discord.Color.red()
    ))
    Blocks.add(user, ctx.author, reason)
    return await ctx.send(embed=discord.Embed(
      description=f"Successfully blocked `{user}`.",
      color=discord.Color.green()
    ))
  
  @commands.guild_only()
  @Checks.reply()
  @commands.command()
  async def unblock(self, ctx, user:Union[discord.User, int]=None):
    if not user: return await ctx.send(embed=discord.Embed(
      description="You must specify a user to unblock.",
      color=discord.Color.red()
    ))
    if isinstance(user, int):
      try:
        user = self.bot.get_user(user)
        user.id
      except Exception as e:
        print(e)
        return await ctx.send(embed=discord.Embed(
          description="You must specify a user to unblock.",
          color=discord.Color.red()
        ))
    if not Blocks.exists(user): return await ctx.send(embed=discord.Embed(
      description="This user is not blocked.",
      color=discord.Color.red()
    ))
    Blocks.delete(user)
    return await ctx.send(embed=discord.Embed(
      description=f"Successfully unblocked `{user}`.",
      color=discord.Color.green()
    ))
  
  @commands.guild_only()
  @Checks.reply()
  @commands.command()
  async def lookup(self, ctx, user:Union[discord.User, int]=None):
    if not user: return await ctx.send(embed=discord.Embed(
      description="You must specify a user to lookup.",
      color=discord.Color.red()
    ))
    if isinstance(user, int):
      try:
        user = self.bot.get_user(user)
        user.id
      except Exception as e:
        print(e)
        return await ctx.send(embed=discord.Embed(
          description="You must specify a user to lookup.",
          color=discord.Color.red()
        ))
    if not Blocks.exists(user): return await ctx.send(embed=discord.Embed(
      description="This user is not blocked.",
      color=discord.Color.red()
    ))
    data = Blocks.get(user)
    return await ctx.send(embed=discord.Embed(
      title=f"Search Results: {user}",
      description=f"This user was blocked by `{self.bot.get_user(data['operator']) or data['operator']}` for `{data['reason']}`.",
      color=discord.Color.green()
    ))

  @block.error
  @unblock.error
  @lookup.error
  async def errorHandler(self, ctx, error):
    if isinstance(error, commands.BadUnionArgument):
      return await ctx.send(embed=discord.Embed(
        description=f"You must enter a valid user.",
        color=discord.Color.red()
      ))
  
def setup(bot):
  bot.add_cog(Block(bot))