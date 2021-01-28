import discord
import asyncio
from core.files import Data
from core import database

from discord.ext import commands

class RecipientReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if isinstance(message.channel, discord.channel.DMChannel) == False:return
        if message.author.bot == True: return


        categories = Data("categories").json_read

        if database.Threads().exists(recipient=message.author.id):
            thread = Threads.get(recipient=message.author.id)
        else:
            descriptions = ''
            for category in categories:
                descriptions += f"{categories[category]['emoji']} {categories[category]['name']}: {categories[category]['description']}\n"

            message = await message.author.send(embed=discord.Embed(title='Createing thread', description=f'Please react to the emoji that corospons to what you need help with\n\n{descriptions}❌ Cancel: Cancel the creation of this thread', color=discord.Color.blurple()))
            reactionList = []
            for category in categories:
                await message.add_reaction(categories[category]['emoji'])
                reactionList.append(categories[category]['emoji'])
            await message.add_reaction('❌')
            reactionList.append('❌')

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in reactionList and reaction.message == message

            while True:
                try:

                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                    if str(reaction.emoji) == "❌":
                        await message.author.send('nice')

                    else:
                        await message.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await message.clear_reactions()
                    await message.edit(content='Timed out, send another message to open a thread', embed=None)
                    return




def setup(bot):
    bot.add_cog(RecipientReply(bot))
