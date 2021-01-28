import discord, asyncio

from core.files import Data
from core import database, embeds

from discord.ext import commands

class RecipientReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.DMChannel) or message.author.bot: return
        
        categories = Data("categories").yaml_read()

        if database.Threads().exists(recipient=message.author.id):
            thread = database.Threads().get(recipient=message.author.id)
            try:
                return await self.bot.get_channel(thread["_id"]).send(embeds.ReplyEmbeds(message).recipientEmbed())
            except Exception as e:
                await message.author.send(embed=embeds.Embeds("There was an error delivering your message. Please report this issue below to the development team.").error(Error=e))
                raise e

        msg = await message.author.send(embed=discord.Embed(
            title="Creating a new thread...",
            description="React to the appropriate category below to create a new thread.\n============================================\n\n" + '\n\n'.join([f"{categories[category]['emoji']} **{category.replace('_', ' ')}** - {categories[category]['description']}" for category in categories]),
            color=discord.Color.green()
        ))

        emojis = [categories[category]['emoji'] for category in categories]

        def is_valid(user, reaction):
            return user.id == message.author.id and reaction.message.id == msg.id and reaction.emoji in emojis
        
        try:
            user, reaction = await self.bot.wait_for('reaction_add', check=is_valid, timeout=60)
        except asyncio.TimeoutError:
            return await message.author.send(embed=embeds.Embeds(":x: Thread creation canceled.").error())
        
        if reaction.emoji == categories["Cancel"]["emoji"]:
            return await message.author.send(embed=embeds.Embeds(":x: Thread creation canceled.").error())
        
        category = self.bot.get_channel(next(categories[x]["category"] for x in categories if categories[x]["emoji"] == reaction.emoji))

        channel = await category.create_text_channel(name=str(message.author), reason="New thread", topic=f"User ID: {message.author.id}")

        await channel.send(embeds.SystemEmbeds.new_thread_embed(message.author, self.bot))

        database.Threads(channel.id).create_thread(recipient=message.author.id, close=None, notify=[], subscribed=[])

        return await message.author.send(embed=embeds.Embeds("Thread successfully created! We have received your message and our support team is on its way! Please remain patient.").success())

def setup(bot):
    bot.add_cog(RecipientReply(bot))