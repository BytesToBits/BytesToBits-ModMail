import datetime, random
from .files import Data
from discord import Embed, Color


class ReplyEmbeds:
    def __init__(self, message):
        self.message = message
        self.config = Data("config").yaml_read()
    
    def recipientEmbed(self):
        embed = Embed(
            description=self.message.content,
            color=Color.green(),
        )

        embed.set_author(name=str(self.message.author), icon_url=self.message.author.avatar_url_as(static_format="png"))
        embed.set_footer(text=f"Recipient Reply • Message ID: {self.message.id}")

        if self.message.attachments:
            embed.add_field(name="Attachments", value=', '.join([f"[{attachment.filename}]({attachment.url})" for attachment in self.message.attachments]))
            images = [attachment.url for attachment in self.message.attachments if attachment.filename.endswith(".png") or attachment.filename.endswith(".jpg") or attachment.filename.endswith(".webp") or attachment.filename.endswith(".gif")]
            if images:
                embed.set_image(url=random.choice(images))
        
        return embed


    def modEmbed(self, anonymous=False):
        embed = Embed(
            description=self.message.content,
            color=Color.blurple(),
        )

        modEmbed = Embed(
            description=self.message.content,
            color=Color.blurple(),
        )

        embed.set_author(name=self.config["anonymous_tag"] if anonymous else str(self.message.author), icon_url=self.config["anonymous_avatar"] if anonymous else self.message.author.avatar_url_as(static_format="png"))
        embed.set_footer(text=self.config["anonymous_footer"] + f" • Message ID: {self.message.id}" if anonymous else self.message.author.top_role.name + f" • Message ID: {self.message.id}")
        if self.message.attachments:
            modEmbed.add_field(name="Attachments", value=', '.join([f"[{attachment.filename}]({attachment.url})" for attachment in self.message.attachments]))
            embed.add_field(name="Attachments", value=', '.join([f"[{attachment.filename}]({attachment.url})" for attachment in self.message.attachments]))
            images = [attachment.url for attachment in self.message.attachments if attachment.filename.endswith(".png") or attachment.filename.endswith(".jpg") or attachment.filename.endswith(".webp") or attachment.filename.endswith(".gif")]
            if images:
                image = random.choice(images)
                embed.set_image(url=image)
                modEmbed.set_image(url=image)

        modEmbed.set_author(name=str(self.message.author), icon_url=self.message.author.avatar_url_as(static_format="png"))
        modEmbed.set_footer(text="Anonymous Reply" + f" • Message ID: {self.message.id}" if anonymous else self.message.author.top_role.name + f" • Message ID: {self.message.id}")

        return (embed, modEmbed)

class SystemEmbeds:
    def new_thread_embed(member, bot):
        embed = Embed(color=Color.green())
        embed.set_author(name=str(member), icon_url=member.avatar_url_as(static_format="png"))
        embed.timestamp = datetime.datetime.utcnow()
        
        config = Data("config").yaml_read()

        guild_member = bot.get_guild(config["main_guild"]).get_member(member.id)

        days_old = datetime.datetime.now() - member.created_at
        member_old = datetime.datetime.now() - guild_member.joined_at

        embed.description = f"{member.mention} created a new thread."

        embed.add_field(name="Account Age", value=f"`ACCOUNT:` {days_old.days} days\n`SERVER:` {member_old.days} days", inline=False)
        embed.add_field(name="Roles", value=', '.join([role.mention for role in guild_member.roles]), inline=False)

        return embed


class Embeds:
    def __init__(self, message):
        self.message = message

    def success(self, **kwargs):
        embed = Embed(
            description=self.message,
            color=Color.green()
        )
        for i in kwargs:
            embed.add_field(name=i.replace("_", " "), value=kwargs[i])
        return embed

    def error(self, **kwargs):
        embed = Embed(
            description=self.message,
            color=Color.red()
        )
        for i in kwargs:
            embed.add_field(name=i.replace("_", " "), value=kwargs[i])
        return embed

    def warn(self, **kwargs):
        embed = Embed(
            description=self.message,
            color=Color.orange()
        )
        for i in kwargs:
            embed.add_field(name=i.replace("_", " "), value=kwargs[i])
        return embed