import discord

from core import database, embeds, checks

commands = discord.ext.commands

class ModReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command(aliases=["r"])
    async def reply(self, ctx, *, message=None):
        if not database.Threads(ctx.channel.id).exists(_id=ctx.channel.id): return
        
        if not ctx.message.attachments: raise commands.MissingRequiredArgument(param="message")

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
    async def anonreply(self, ctx, *, message):
        if not database.Threads(ctx.channel.id).exists(_id=ctx.channel.id): return
        
        thread = database.Threads(ctx.channel.id).data()
        recipient = self.bot.get_user(thread["recipient"])
        logs = database.Logs(ctx.channel.id)

        ctx.message.content = message
        replyEmbeds = embeds.ReplyEmbeds(ctx.message).modEmbed(anonymous=True)
        await recipient.send(embed=replyEmbeds[0])
        await ctx.message.delete()
        await ctx.send(embed=replyEmbeds[1])
        return logs.add_message(ctx.message, mod=True)
    

def setup(bot):
    bot.add_cog(ModReply(bot))