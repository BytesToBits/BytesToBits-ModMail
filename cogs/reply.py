import discord
import asyncio
from core.files import Data
from core import database
import time
from discord.ext import commands

class RecipientReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if isinstance(message.channel, discord.channel.DMChannel) == False:return
        if message.author.bot: return
        if message.author == self.bot.user: return



        categories = Data("categories").json_read

        if database.Threads().exists(recipient=message.author.id):
            thread = Threads.get(recipient=message.author.id)
        else:
            descriptions = ''
            for category in categories:
                descriptions += f"{categories[category]['emoji']} {categories[category]['name']}: {categories[category]['description']}\n"

            msg = await message.author.send(embed=discord.Embed(title='Createing thread', description=f'Please react to the emoji that corospons to what you need help with\n\n{descriptions}❌ Cancel: Cancel the creation of this thread', color=discord.Color.blurple()))
            reactionList = []
            for category in categories:
                await msg.add_reaction(categories[category]['emoji'])
                reactionList.append(categories[category]['emoji'])
            await msg.add_reaction('❌')
            reactionList.append('❌')

            def check(reaction, user):
                print(message.author)
                print(user)
                print(user.bot == False)
                return user.bot == False

            while True:
                print('test')
                reaction, user = await self.bot.wait_for('reaction_add', timeout=50, check=check)
                print('test2')




def setup(bot):
    bot.add_cog(RecipientReply(bot))
