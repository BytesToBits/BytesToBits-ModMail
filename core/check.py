from .files import Data
from discord.ext import commands

config = Data("config").json_read

def manager():
    def predicate(ctx):
        return ctx.author.id in config["managers"]
    return commands.check(predicate)

def canReply():
    def predicate(ctx):
        if not ctx.guild or not ctx.guild.id == config["support_guild"]: return False
        if ctx.guild.get_role(config["support_role"]) in ctx.author.roles: return True
        else: return False
    return commands.check(predicate)
