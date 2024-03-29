import discord, asyncio

from core.files import Data
from core import database, embeds

from discord.ext import commands

class RecipientReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.creating = []
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.DMChannel) or message.author.bot: return
        if message.author in self.creating: return
        if database.Blocks(message.author.id).blocked: return
        categories = Data("categories").yaml_read()

        if database.Threads().exists(recipient=message.author.id):
            thread = database.Threads().get(recipient=message.author.id)
            if thread['close']:
                database.Threads(thread["_id"]).update_thread(close=None)
            try:
                database.Logs(thread["_id"]).add_message(message)
                await self.bot.get_channel(thread["_id"]).send(embed=embeds.Embeds("Close canceled due to new reply.").warn())
                content = None
                if thread["notify"]:
                    content = ' '.join(thread["notify"])
                if thread["subscribed"]:
                    if not content: content = ""
                    content += " " + ' '.join(thread["subscribed"])
                await self.bot.get_channel(thread["_id"]).send(content=content, embed=embeds.ReplyEmbeds(message).recipientEmbed())
                return database.Threads(thread["_id"]).update_thread(notify=[])
            except Exception as e:
                await message.author.send(embed=embeds.Embeds("There was an error delivering your message. Please report this issue below to the development team.").error(Error=f"```py\n{e}```"))
                raise e
        self.creating.append(message.author)
        msg = await message.author.send(embed=discord.Embed(
            title="Creating a new thread...",
            description="React to the appropriate category below to create a new thread.\n============================================\n\n" + '\n\n'.join([f"{categories[category]['emoji']} **{category.replace('_', ' ')}** - {categories[category]['description']}" for category in categories]),
            color=discord.Color.green()
        ))

        emojis = [categories[category]['emoji'] for category in categories]

        for emoji in emojis: await msg.add_reaction(emoji)

        def is_valid(reaction, user):
            return user.id == message.author.id and reaction.message.id == msg.id and reaction.emoji in emojis
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=is_valid, timeout=60)
        except asyncio.TimeoutError:
            self.creating.remove(message.author)
            await msg.delete()
            return await message.author.send(embed=embeds.Embeds(":x: Thread creation canceled.").error())
        
        if reaction.emoji == categories["Cancel"]["emoji"]:
            self.creating.remove(message.author)
            await msg.delete()
            return await message.author.send(embed=embeds.Embeds(":x: Thread creation canceled.").error())
        
        category = self.bot.get_channel(next(categories[x]["category"] for x in categories if categories[x]["emoji"] == reaction.emoji))

        channel = await category.create_text_channel(name=str(message.author).replace("#", "-"), reason="New thread", topic=f"User ID: {message.author.id}")

        await channel.send(content=next(categories[category]["mention"] for category in categories if categories[category]["emoji"] == reaction.emoji),embed=embeds.SystemEmbeds.new_thread_embed(message.author, self.bot))

        database.Threads(channel.id).create_thread(recipient=message.author.id, close=None, notify=[], subscribed=[])

        database.Logs(channel.id).add_message(message)

        self.creating.remove(message.author)

        await channel.send(embed=embeds.ReplyEmbeds(message).recipientEmbed())

        await msg.delete()

        return await message.author.send(embed=embeds.Embeds("Thread successfully created! We have received your message and our support team is on its way! Please remain patient.").success())

def setup(bot):
    bot.add_cog(RecipientReply(bot))