import discord

from core.database import Threads

commands = discord.ext.commands

class RecipientTypeSynch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if not isinstance(channel, discord.DMChannel): return
        if not Threads(channel.id).exists: return
        
        thread = Threads(channel.id).get(recipient=user.id)

        return await self.bot.get_channel(thread["_id"]).trigger_typing()

def setup(bot):
    bot.add_cog(RecipientTypeSynch(bot))