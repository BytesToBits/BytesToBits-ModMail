import discord, inspect

from core import database, embeds, checks
from core.files import Data

commands = discord.ext.commands

class ModReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command(aliases=["r"])
    async def reply(self, ctx, *, message=None):
        if not database.Threads(ctx.channel.id).exists(_id=ctx.channel.id): return
        
        if not message and not ctx.message.attachments: raise commands.MissingRequiredArgument(inspect.Parameter(name="message", kind=inspect.Parameter.POSITIONAL_ONLY))

        thread = database.Threads(ctx.channel.id).data()
        recipient = self.bot.get_user(thread["recipient"])
        logs = database.Logs(ctx.channel.id)

        ctx.message.content = message
        replyEmbeds = embeds.ReplyEmbeds(ctx.message).modEmbed()
        await recipient.send(embed=replyEmbeds[0])
        await ctx.message.delete()
        await ctx.send(embed=replyEmbeds[1])
        return logs.add_message(ctx.message, mod=True)
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command(aliases=["ar"])
    async def anonreply(self, ctx, *, message=None):
        if not database.Threads(ctx.channel.id).exists(_id=ctx.channel.id): return
        
        if not message and not ctx.message.attachments: raise commands.MissingRequiredArgument(inspect.Parameter(name="message", kind=inspect.Parameter.POSITIONAL_ONLY))
        
        thread = database.Threads(ctx.channel.id).data()
        recipient = self.bot.get_user(thread["recipient"])
        logs = database.Logs(ctx.channel.id)

        ctx.message.content = message
        replyEmbeds = embeds.ReplyEmbeds(ctx.message).modEmbed(anonymous=True)
        await recipient.send(embed=replyEmbeds[0])
        await ctx.message.delete()
        await ctx.send(embed=replyEmbeds[1])
        return logs.add_message(ctx.message, mod=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel): return
        if not database.Threads().exists(_id=message.channel.id): return
        
        config = Data("config").yaml_read()

        if not message.guild.get_role(config["support_role"]) in message.author.roles: return

        if not message.content: return

        content = message.content.split(" ")[0]

        if content.startswith(config["prefix"]*3):
            anonymous=True
        elif content.startswith(config["prefix"]*2):
            anonymous=False
        else: return

        content = content.replace(config["prefix"], "")

        if not database.Snippets().get(_id=content): return

        content = database.Snippets().get(_id=content)['content']

        thread = database.Threads(message.channel.id).data()
        recipient = self.bot.get_user(thread["recipient"])
        logs = database.Logs(message.channel.id)

        message.content = content
        replyEmbeds = embeds.ReplyEmbeds(message).modEmbed(anonymous=anonymous)
        await recipient.send(embed=replyEmbeds[0])
        await message.delete()
        await message.channel.send(embed=replyEmbeds[1])
        return logs.add_message(message, mod=True)
        

def setup(bot):
    bot.add_cog(ModReply(bot))