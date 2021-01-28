import discord, yaml
from Admin.admin import Files, Checks
from Admin.database import Threads

commands = discord.ext.commands

class Utils(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(name="id")
  async def _id(self, ctx):
    channel = ctx.channel
    if not Threads.exists(channel): return
    return await ctx.send(Threads.get(channel)['recipient'])

  @commands.guild_only()
  @Checks.owner()
  @commands.command()
  async def activity(self, ctx, activity=None, *, name=None):
    if not activity or not name or not activity.lower() in ["playing", "watching", "listening_to"]:
      return await ctx.send(embed=discord.Embed(
        description="You must mention an activity type and a status.\nAvailable types: `playing`, `watching`, `listening_to`",
        color=discord.Color.red()
      ))
    if activity.lower() == "watching":
      code = 1
      at = discord.ActivityType.watching
    elif activity.lower() == "listening_to":
      code = 2
      at = discord.ActivityType.listening
    else:
      code = 0
      at = discord.ActivityType.playing
    await self.bot.change_presence(activity=discord.Activity(type=at, name=name))
    config = Files.get("config")
    config['status'] = {
      "name":name,
      "type":code
    }
    with open("Admin/config.yml", "w") as f:
      yaml.dump(config, f)
    return await ctx.send(embed=discord.Embed(
      description="Successfully updated bot status.",
      color=discord.Color.green()
    ))

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound): return
    raise error

def setup(bot):
  bot.add_cog(Utils(bot))