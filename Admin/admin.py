import yaml
from discord.ext import commands

class Files:
  def config(a, b):
    with open("Admin/config.yml", "r") as f:
      return yaml.load(f, Loader=yaml.FullLoader)[a][b]
  
  def read(path):
    with open(path, "r") as f:
      return f.read()

  def get(file):
    with open(f"Admin/{file}.yml", "r") as f:
      return yaml.load(f, Loader=yaml.FullLoader)

  def emoji(emoji):
    return Files.config("emojis", emoji)

class Checks:
  def owner():
    def predicate(ctx):
      return ctx.author.id in Files.config("main", "managers")
    return commands.check(predicate)
    
  def modmail_server():
    def predicate(ctx):
      return ctx.guild.id != None and ctx.guild.id == Files.get("support")["modmail_guild_id"]
    return commands.check(predicate)

  def reply():
    def predicate(ctx):
      return ctx.guild.get_role(Files.get("support")["support_role"]) in ctx.author.roles or ctx.author.id in Files.config("main", "managers")
    return commands.check(predicate)