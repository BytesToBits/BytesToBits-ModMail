import discord, asyncio

from core.database import Snippets
from core import embeds, checks

commands = discord.ext.commands

class SnippetManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @checks.canReply()
    @commands.group(name="snippets", aliases=["snippet", "s"], case_insensitive=True, invoke_without_command=True)
    async def snippets(self, ctx, snippetName=None):
        if not ctx.author.guild_permissions.administrator: return
        if not snippetName:
            snippets = Snippets().get_all()
            return await ctx.send(embed=discord.Embed(
                title="Available Snippets",
                description=','.join([f"`{snippet['_id']}`" for snippet in snippets]),
                color=discord.Color.green()
            ))
        if not Snippets().get(_id=snippetName): return await ctx.send(embed=embeds.Embeds("This snippet does not exist.").error())

        return await ctx.send(embed=discord.Embed(
            title=f"Snippet Preview | {snippetName}",
            description=Snippets().get(_id=snippetName)['content'],
            color=discord.Color.green()
        ))
    
    @commands.guild_only()
    @checks.canReply()
    @snippets.command(name="add", aliases=["create"])
    async def snippet_add(self, ctx, snippetName, *, content):
        if not ctx.author.guild_permissions.administrator: return

        if Snippets().get(_id=snippetName):
            emojis = ["✅", "❌"]

            msg = await ctx.send(embed=embeds.Embeds("This snippet already exists, replace?").warn())

            for emoji in emojis: await msg.add_reaction(emoji)

            def is_valid(reaction, user):
                return reaction.message.id == msg.id and reaction.emoji in emojis and user.id == ctx.author.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=is_valid, timeout=60)
            except asyncio.TimeoutError:
                return await msg.delete()
            
            if reaction.emoji == emojis[1]:
                return await ctx.send(embed=embeds.Embeds("Snippet creation canceled.").error())

            Snippets().delete_snippet(snippetName)

        Snippets().add_snippet(snippetName, content)

        return await ctx.send(embed=embeds.Embeds(f"Snippet `{snippetName}` successfully created!").success())

    @commands.guild_only()
    @checks.canReply()
    @snippets.command(name="remove", aliases=["delete", "del"])
    async def snippet_delete(self, ctx, snippetName):
        if not ctx.author.guild_permissions.administrator: return
        if not Snippets().get(_id=snippetName): return await ctx.send(embed=embeds.Embeds("This snippet does not exist.").error())
        Snippets().delete_snippet(snippetName)
        return await ctx.send(embed=embeds.Embeds("Snippet successfully deleted!").success())


def setup(bot):
    bot.add_cog(SnippetManagement(bot))