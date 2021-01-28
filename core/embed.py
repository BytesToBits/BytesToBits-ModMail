
import datetime, random
from .files import Data
from discord import Embed, Color, Message


class ReplyEmbeds:
    def __init__(self, message):
        self.message = message
        self.config = Data("config").json_read

    def recipientEmbed(self):
        embed = Embed(
            description=message.content,
            color=Color.green(),
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_author(name=str(self.message.author), icon_url=self.message.author.avatar_url_as(static_format="png"))
        embed.set_footer(text="Recipient Reply")

        if self.message.attachments:
            embed.add_field(name="Attachments", value=', '.join([f"[{attachment.filename}]({attachment.url})" for attachment in self.message.attachments]))
            images = [attachment.url for attachment in self.message.attachments if attachment.filename.endswith(".png") or attachment.filename.endswith(".jpg") or attachment.filename.endswith(".webp") or attachment.filename.endswith(".gif")]
            if images:
                embed.set_image(url=random.choice(images))

        return embed


    def modEmbed(self, anonymous=False):
        embed = Embed(
            description=message.content,
            color=Color.blurple(),
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_author(name=self.config["anonymous_tag"] if anonymous else str(message.author), icon_url=config["anonymous_avatar"] if anonymous else self.message.author.avatar_url_as(static_format="png"))
        embed.set_footer(text=self.config["anonymous_footer"] if anonymous else self.message.author.top_role.name)

        if self.message.attachments:
            embed.add_field(name="Attachments", value=', '.join([f"[{attachment.filename}]({attachment.url})" for attachment in self.message.attachments]))
            images = [attachment.url for attachment in self.message.attachments if attachment.filename.endswith(".png") or attachment.filename.endswith(".jpg") or attachment.filename.endswith(".webp") or attachment.filename.endswith(".gif")]
            if images:
                embed.set_image(url=random.choice(images))

        mod_embed = embed
        mod_embed.set_author(name=str(self.message.author), icon_url=self.message.author.avatar_url_as(static_format="png"))
        return (embed, mod_embed)

def success(m, **kwargs):
    embed = Embed(
        description=m,
        color=Color.green()
    )
    for i in kwargs:
        embed.add_field(name=i.replace("_", " "), value=kwargs[i])
    return embed

def error(m, **kwargs):
    embed = Embed(
        description=m,
        color=Color.red()
    )
    for i in kwargs:
        embed.add_field(name=i.replace("_", " "), value=kwargs[i])
    return embed

def warn(m, **kwargs):
    embed = Embed(
        description=m,
        color=Color.orange()
    )
    for i in kwargs:
        embed.add_field(name=i.replace("_", " "), value=kwargs[i])
    return embed
