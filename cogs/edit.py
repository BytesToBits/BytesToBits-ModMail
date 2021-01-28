import discord
from Admin.database import Threads
from Admin.admin import Checks

commands = discord.ext.commands

class Edit(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.guild_only()
  @Checks.modmail_server()
  @Checks.reply()
  @commands.command()
  async def edit(self, ctx, msgid=None, *, message=None):
    channel = ctx.channel
    if not Threads.exists(channel): return
    if not msgid: return
    try:
      int(msgid)
    except:
      message = str(msgid + " " + (message or ""))
      msgid = None
    
    if not message: return await ctx.send(embed=discord.Embed(
      description=f"Message content cannot be None.",
      color=discord.Color.red()
    ))

    messages = Threads.get(channel)["messages"]
    try:
      if not msgid:
        async for i in channel.history(limit=100):
          if i.author.id == self.bot.user.id:
            embed = next(i for i in i.embeds)
            if str(i.id) in messages and not embed.footer.text.startswith("Recipient"):
              key = str(i.id)
              break
        else:
          return await ctx.send(embed=discord.Embed(
            description="Cannot find message to edit.",
            color=discord.Color.red()
          ))
        msg = await channel.fetch_message(int(key))
        embed = next(i for i in msg.embeds)
        embed.description = message
        await msg.edit(embed=embed)
        async for i in self.bot.get_user(Threads.get(channel)['recipient']).history():
          if i.id == messages[key]:
            msg = i
            break
        else:
          return await ctx.send("Cannot find message to edit in recipient's DMs.")
        embed = next(i for i in msg.embeds)
        embed.description = message
        await msg.edit(embed=embed)
        return await ctx.message.add_reaction("✅")
      else:
        msg = await channel.fetch_message(int(msgid))
        embed = next(i for i in msg.embeds)
        if not embed.color==discord.Color.blurple(): return await ctx.send(embed=discord.Embed(
          description="You cannot edit this embed.",
          color=discord.Color.red()
        ))
        embed.description = message
        await msg.edit(embed=embed)
        msg = await self.bot.get_user(Threads.get(channel)['recipient']).fetch_message(messages[msgid])
        embed = next(i for i in msg.embeds)
        embed.description = message
        await msg.edit(embed=embed)
        return await ctx.message.add_reaction("✅")
    except Exception as e:
      await ctx.send(embed=discord.Embed(
        description=f"```{e}```",
        color=discord.Color.red()
      ))
      raise e

  @commands.Cog.listener()
  async def on_raw_message_edit(self, payload):
    message_id = payload.message_id
    channel_id = payload.channel_id
    message = await self.bot.get_channel(channel_id).fetch_message(message_id)
    if message.author.bot: return
    thread = Threads.find({"channel":channel_id})
    if not thread: return
    messages = thread['messages']
    for i in messages:
      if messages[i] == message_id:
        key = i
        break
    else:
      return
    channel = self.bot.get_channel(thread['_id'])
    mes = await channel.fetch_message(int(key))
    embed = next(i for i in mes.embeds)
    old = embed.description
    embed.description = payload.data['content']
    embed.add_field(name="**Former Message**", value=old)
    return await mes.edit(embed=embed)
    

def setup(bot):
  bot.add_cog(Edit(bot))