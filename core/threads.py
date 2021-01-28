import discord
from Admin.admin import Files

def recipient_embed(message):
  embed = discord.Embed(
      description=message.content,
      color=discord.Color.green()
    )
  embed.set_author(name=str(message.author), icon_url=message.author.avatar_url_as(static_format="png"))
  embed.set_footer(text=f"Recipient Reply • Message ID: {message.id}")
  if not len(message.attachments) == 0:
    embed.set_image(url=message.attachments[0].url)
    embed.add_field(name="Attachments", value=', '.join(f"[{i.filename}]({i.url})" for i in message.attachments))
  return embed
  
def mod_embed(msg, message, anonymous=False):
  embed = discord.Embed(description=message, color=discord.Color.blurple())
  modembed = discord.Embed(description=message, color=discord.Color.blurple())
  if anonymous:
    embed.set_footer(text=f"Reply • Message ID: {msg.id}")
    modembed.set_footer(text=f"Anonymous Reply • Message ID: {msg.id}")
    embed.set_author(name="Staff Team", icon_url="https://i.imgur.com/kaxP5Cn.gif")
  else:
    embed.set_footer(text=f"{msg.author.top_role.name} • Message ID: {msg.id}")
    modembed.set_footer(text=f"{msg.author.top_role.name} • Message ID: {msg.id}")
    embed.set_author(name=str(msg.author), icon_url=msg.author.avatar_url_as(static_format="png"))
  if not len(msg.attachments) == 0:
    embed.set_image(url=msg.attachments[0].url)
    embed.add_field(name="Attachments", value=', '.join(f"[{i.filename}]({i.url})" for i in msg.attachments))
    modembed.set_image(url=msg.attachments[0].url)
    modembed.add_field(name="Attachments", value=', '.join(f"[{i.filename}]({i.url})" for i in msg.attachments))
  modembed.set_author(name=str(msg.author), icon_url=msg.author.avatar_url_as(static_format="png"))
  
  return embed, modembed