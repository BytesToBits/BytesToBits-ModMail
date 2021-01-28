import discord
from Admin.database import Snippets

commands = discord.ext.commands

class SnippetsHandler(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.guild_only()
  @commands.group(name="snippet",aliases=["snippets", "s"],invoke_without_command=True)
  async def snippet(self, ctx, name=None):
    if not name:
      if Snippets.get_all() == None or len(Snippets.get_all()) == 0:
        return await ctx.send(embed=discord.Embed(
          description="There are no available snippets.",
          color=discord.Color.red()
        )) 
      return await ctx.send(embed=discord.Embed(
        title="Available Snippets",
        description='\n'.join([i["_id"] for i in Snippets.get_all()]),
        color=discord.Color.blurple()
      ))
    else:
      snippets = [i["_id"] for i in Snippets.get_all()]
      if name.lower() not in snippets:
        return await ctx.send(embed=discord.Embed(
          description=f"Snippet `{name}` does not exist.",
          color=discord.Color.red()
        ))
      return await ctx.send(embed=discord.Embed(
        title=f"Snippet Preview: {name}",
        description=Snippets.get(name.lower())["content"],
        color=discord.Color.blurple()
      ))
  
  @commands.guild_only()
  @snippet.command(name="add", aliases=["append", "create"])
  @commands.has_permissions(manage_guild=True)
  async def snippet_add(self, ctx, name=None, *, content=None):
    if not name or not content:
      return await ctx.send(embed=discord.Embed(
        description="Snippet name and snippet content are required for this command.",
        color=discord.Color.red()
      ))
    snippets = [i["_id"] for i in Snippets.get_all()]
    if not name.lower() in snippets:
      Snippets.add(name.lower(), content)
      return await ctx.send(embed=discord.Embed(
        description=f"Snippet `{name}` created.",
        color=discord.Color.green()
      ))
    else:
      msg = await ctx.send(embed=discord.Embed(
        title="Replace Snippet",
        description="This snippet already exists. **Replace?**",
        color=discord.Color.orange()
      ))
      await msg.add_reaction("✅")
      await msg.add_reaction("❌")
      def check(reaction, user):
        return reaction.emoji in ["✅", "❌"] and reaction.message.id == msg.id and user.id == ctx.author.id
      try:
        reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
      except:
        await msg.edit(embed=discord.Embed(
          description="Snippet replacement canceled.",
          color=discord.Color.red()
        ))
        return await msg.remove_reaction("✅", self.bot.user)
      if reaction.emoji == "❌":
        return await ctx.send(embed=discord.Embed(
          description="Snippet replacement canceled.",
          color=discord.Color.red()
        ))
      Snippets.update(name.lower(), content)
      return await ctx.send(embed=discord.Embed(
        description=f"Snippet `{name}` successfully replaced.",
        color=discord.Color.green()
      ))

  @commands.guild_only()
  @snippet.command(aliases=["remove", "delete"])
  @commands.has_permissions(manage_guild=True)
  async def snippet_delete(self, ctx, name=None):
    if not name: return await ctx.send(embed=discord.Embed(
      description="You must mention a snippet name to delete.",
      color=discord.Color.red()
    ))
    snippets = [i["_id"] for i in Snippets.get_all()]
    if not name.lower() in snippets:
      return await ctx.send(embed=discord.Embed(
        description="This snippet does not exist.",
        color=discord.Color.red()
      ))
    Snippets.delete(name.lower())
    return await ctx.send(embed=discord.Embed(
      description=f"Snippet `{name}` deleted.",
      color=discord.Color.green()
    ))

def setup(bot):
  bot.add_cog(SnippetsHandler(bot))