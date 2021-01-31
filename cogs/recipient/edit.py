import discord

from core import database

commands = discord.ext.commands

class RecipientMessageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not isinstance(after.channel, discord.DMChannel) or after.author.bot: return
        if not database.Threads().exists(recipient=after.author.id): return

        thread = database.Threads().get(recipient=after.author.id)

        logs = database.Logs(thread["_id"])

        if not logs.get(_id=after.id): return

        logs.edit_message(after)

        channel = self.bot.get_channel(thread["_id"])

        async for message in channel.history():
            if message.embeds:
                embed = next(embed for embed in message.embeds if embed.footer.text != discord.Embed.Empty)
                if embed.footer.text.find(str(after.id)) != -1:
                    msg = message
                    break
        else:
            return
        
        embed.clear_fields()
        embed.add_field(name="Former Message", value=before.content)
        embed.description = after.content

        return await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(RecipientMessageEdit(bot))