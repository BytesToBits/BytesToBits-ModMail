import discord

from core.files import Data
from core import database

from discord.ext import commands

class RecipientReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message, discord.DMChannel): return
        
        categories = Data("categories").json_read

        if database.Threads.exists(recipient=message.author.id):
            thread = Threads.get(recipient=message.author.id)
