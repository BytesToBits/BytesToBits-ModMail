from Admin.admin import Files
from Admin.database import Threads, Blocks
from core import threads
import discord, asyncio, datetime

commands = discord.ext.commands

class NewThreads(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if not isinstance(message.channel, discord.DMChannel) or message.author.bot: return
    if Blocks.exists(message.author): return
    if Threads.find({"recipient":message.author.id}): return
    categories = Files.get("support")["categories"]
    desc = "\n\n".join([f"{categories[i]['reaction']} - {categories[i]['description']}" for i in categories])
    member = message.author
    msg = await member.send(embed=discord.Embed(
      title="Creating a new thread...",
      description=
f"""Please choose one of the following categories to create a new thread in!
==================================
{desc}

:x: - Cancel thread creation.""",
      color=discord.Color.green()
    ))

    for x in [categories[i]['reaction'] for i in categories] + ["❌"]:
      await msg.add_reaction(x)

    def check(reaction, user):
      return reaction.message.id == msg.id and user.id == member.id and reaction.emoji in [categories[i]['reaction'] for i in categories] + ["❌"]
    
    try:
      reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60)
    except asyncio.TimeoutError:
      await msg.delete()
      return await member.send(embed=discord.Embed(
        description=":fire: Thread creation canceled due to timeout.",
        color=discord.Color.orange()
      ))
    if reaction.emoji not in [categories[i]['reaction'] for i in categories]:
      return await member.send(embed=discord.Embed(
        description=":x: Thread creation canceled.",
        color=discord.Color.red()
      ))
    name = next(categories[i]["name"] for i in categories if categories[i]["reaction"] == reaction.emoji)
    category = next(self.bot.get_guild(Files.get("support")["modmail_guild_id"]).get_channel(categories[i]["id"]) for i in categories if categories[i]["reaction"] == reaction.emoji)
    channel = await category.create_text_channel(name=f"{member.name}-{member.discriminator}", topic=f"User ID: {member.id}")
    await channel.send(content=Files.get("support")["mention"], embed=discord.Embed(
      description=f"{member.mention} created a new thread in the **{name}** category. Their account was created {(datetime.datetime.now()-member.created_at).days} days ago and joined {(datetime.datetime.now()-self.bot.get_guild(Files.get('support')['main_guild_id']).get_member(member.id).joined_at).days} days ago.",
      color=discord.Color.purple()
    )
    .set_author(name=str(member), icon_url=member.avatar_url_as(static_format="png")))
    mes = await channel.send(embed=threads.recipient_embed(message))
    Threads.add(channel, message)
    Threads.add_message(channel, message, mes)
    await msg.delete()
    return await member.send(embed=discord.Embed(
      title="Thread Created",
      description=Files.get("support")["thread_creation_message"].format(name),
      color=discord.Color.green()
    ))

def setup(bot):
  bot.add_cog(NewThreads(bot))
