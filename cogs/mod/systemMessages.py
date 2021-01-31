import discord

from core.files import Data
from core.database import Threads, Logs

commands = discord.ext.commands

class SystemMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or isinstance(message.channel, discord.DMChannel): return

        config = Data("config").yaml_read()

        if message.content.startswith(config["prefix"]): return

        if not Threads().exists(_id=message.channel.id): return

        logs = Logs(message.channel.id)

        logs.add_message(message, system=True)

    @commands.Cog.listener()
    async def on_message_edit(self, message, after):
        if message.author.bot or isinstance(message.channel, discord.DMChannel): return

        if message.content == after.content: return

        config = Data("config").yaml_read()

        if message.content.startswith(config["prefix"]): return

        if not Threads().exists(_id=message.channel.id): return

        logs = Logs(message.channel.id)

        logs.edit_message(after)
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or isinstance(message.channel, discord.DMChannel): return

        config = Data("config").yaml_read()

        if message.content.startswith(config["prefix"]): return

        if not Threads().exists(_id=message.channel.id): return

        logs = Logs(message.channel.id)

        logs.delete_message(message)

def setup(bot):
    bot.add_cog(SystemMessages(bot))