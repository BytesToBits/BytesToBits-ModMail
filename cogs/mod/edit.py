import discord

from core import database, embeds, checks

commands = discord.ext.commands

class ModEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.guild_only()
    @checks.canReply()
    @commands.command()
    async def edit(self, ctx, *, content):
        if not database.Threads().exists(_id=ctx.channel.id): return

        try:
            messageID = int(content.split(" ")[0])
            message = await ctx.channel.fetch_message(messageID)
            if not message.author.id == self.bot.user.id or not message.embeds: return await ctx.send(embed=embeds.Embeds("You can only edit reply messages.").error())
            embed = next(embed for embed in message.embeds)
            if embed.color != discord.Color.blurple() or embed.footer.text == discord.Embed.Empty: return await ctx.send(embed=embeds.Embeds("Message not found.").error())
            messageID = int(embed.footer.text.split(" ")[-1])
            embed.description = ' '.join(content.split(" ")[1:])
            await message.edit(embed=embed)
            user = self.bot.get_user(database.Threads().get(_id=ctx.channel.id)["recipient"])
            
            def predicate(message):
                if not message.author.id == self.bot.user.id or not message.embeds: return False
                embed = next(embed for embed in message.embeds)
                if embed.color != discord.Color.blurple() or embed.footer.text == discord.Embed.Empty: return False
                if embed.footer.text.split(" ")[-1] == str(messageID): return True
                return False

            message = await user.history().find(predicate)

            embed = next(embed for embed in message.embeds)

            embed.description = ' '.join(content.split(" ")[1:])
            
            await message.edit(embed=embed)

            message.id = messageID
            message.content = ' '.join(content.split(" ")[1:])

            database.Logs(ctx.channel.id).edit_message(message)

            return await ctx.message.add_reaction("✅")

        except:
            def predicate(message):
                if not message.author.id == self.bot.user.id: return False
                embed = next(embed for embed in message.embeds)
                if embed.color != discord.Color.blurple() or embed.footer.text == discord.Embed.Empty: return False
                return True
            
            message = await ctx.channel.history().find(predicate)
            embed = next(embed for embed in message.embeds)
            embed.description = content
            await message.edit(embed=embed)

            user = self.bot.get_user(database.Threads().get(_id=ctx.channel.id)["recipient"])

            message = await user.history().find(predicate)
            embed = next(embed for embed in message.embeds)
            embed.description = content
            await message.edit(embed=embed)

            messageID = int(embed.footer.text.split(" ")[-1])

            message.id = messageID
            message.content = content

            database.Logs(ctx.channel.id).edit_message(message)

            return await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(ModEdit(bot))