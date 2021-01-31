import discord

from core import database, embeds, checks

commands = discord.ext.commands

class ModDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command()
    async def delete(self, ctx, messageID=None):
        if not database.Threads().exists(_id=ctx.channel.id): return

        def predicate(message):
            if message.author.id != self.bot.user.id or not message.embeds: return False
            embed = next(embed for embed in message.embeds)
            if embed.color != discord.Color.blurple() or embed.footer.text == discord.Embed.Empty: return False
            return True

        thread = database.Threads(ctx.channel.id)
        user = self.bot.get_user(thread.get(_id=ctx.channel.id)["recipient"])

        if not messageID:
            message = await ctx.channel.history().find(predicate)
        else:
            try:
                message = await ctx.channel.fetch_message(int(messageID))
                if message.author.id != self.bot.user.id or not message.embeds:
                    return await ctx.send(embed=embeds.Embeds("Message not found.").error())
                embed = next(embed for embed in message.embeds)
                if embed.color != discord.Color.blurple() or embed.footer.text == discord.Embed.Empty:
                    return await ctx.send(embed=embeds.Embeds("Message not found.").error())
            except:
                return await ctx.send(embed=embeds.Embeds("Message not found.").error())
        
        embed = next(embed for embed in message.embeds)

        messageID = int(embed.footer.text.split(" ")[-1])

        def get_user_message(message):
            if message.author.id != self.bot.user.id or not message.embeds: return False
            embed = next(embed for embed in message.embeds)
            if embed.color != discord.Color.blurple() or embed.footer.text == discord.Embed.Empty: return False
            if embed.footer.text.find(str(messageID)) != -1: return True
            return False
        
        userMessage = await user.history().find(get_user_message)

        database.Logs(ctx.channel.id).delete_message(message, messageID)

        await userMessage.delete()

        await message.delete()

        return await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(ModDelete(bot))