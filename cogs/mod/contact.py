import discord

from core import database, embeds, checks, files

commands = discord.ext.commands

class Contact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command()
    async def contact(self, ctx, user:discord.User=None):
        if not user or user.bot: user = ctx.author
        if database.Threads().exists(recipient=user.id):
            return await ctx.send(embed=embeds.Embeds("A thread already exists for this user!").error())
        
        categories = files.Data("categories").yaml_read()

        category = self.bot.get_channel(categories["General"]["category"])

        channel = await category.create_text_channel(name=str(user).replace("#", "-"), reason="New thread", topic=f"User ID: {user.id}")

        await channel.send(content=categories["General"]["mention"],embed=embeds.SystemEmbeds.new_thread_embed(user, self.bot))

        database.Threads(channel.id).create_thread(recipient=user.id, close=None, notify=[], subscribed=[])

        return await ctx.send(embed=embeds.Embeds(f"Thread created! ({channel.mention})").success())

def setup(bot):
    bot.add_cog(Contact(bot))