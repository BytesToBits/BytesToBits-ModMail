import discord

from core import database

commands = discord.ext.commands

class RecipientMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not isinstance(message.channel, discord.DMChannel) or message.author.bot: return
        if not database.Threads().exists(recipient=message.author.id): return

        thread = database.Threads().get(recipient=message.author.id)

        channel = self.bot.get_channel(thread["_id"])

        async for mes in channel.history():
            if mes.embeds:
                embed = next(embed for embed in mes.embeds if embed.footer.text != discord.Embed.Empty)
                if embed.footer.text.find(str(message.id)) != -1:
                    msg = mes
                    break
        else:
            return
        
        embed.set_author(name= embed.author.name + " (Original Message Deleted)", icon_url=embed.author.icon_url)
        embed.description = message.content

        return await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(RecipientMessageDelete(bot))