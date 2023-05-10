# standard
import nextcord, requests, re, random, string
from typing import Literal

# nextcord
from nextcord import Embed
from nextcord.ext import commands
from nextcord.ext.commands import ( Context, )

# local
import config

def blockquote(
    string: str
) -> str:
    """Add blockquotes to a string"""
    # inserts > at the start of string and after new lines
    # as long as it is not at the end of the string
    return re.sub(r"(^|\n)(?!$)", r"\1> ", string.strip())

def s(data) -> Literal["", "s"]:
    if isinstance(data, str):
        data = int(not data.endswith("s"))
    elif hasattr(data, "__len__"):
        data = len(data)
    check = data != 1
    return "s" if check else ""

def custom_id(
    view: str, 
    id: int
) -> str:
    """create a custom id from the bot name : the view : the identifier"""
    return f"{config.BOT_NAME}:{view}:{id}"

def button_custom_id(
    id: str, 
    name: int
) -> str:
    """create a custom id from the bot name : the view : the identifier"""
    return f"{id}:{name}"

def embed_success(
    title: str,
    description: str = None,
    colour: nextcord.Colour = nextcord.Colour.green(),
) -> Embed:
    """Embed a success message and an optional description"""
    embed = Embed(title=title, colour=colour)
    if description:
        embed.description = description
    return embed

def embed_store(
    ctx: Context,
    title: str = None,
    description: str = None,
    colour: nextcord.Colour = config.theme_color,
) -> Embed:
    """Embed with preset author, footer and an optional description"""
    embed = Embed(
        colour=colour
    ).set_author(
        name=ctx.guild.name, 
        icon_url = ctx.guild.icon
    ).set_footer(
        text=config.footer_str, 
        icon_url=config.author_url
    )
    if title:
        embed.title = title
    if description:
        embed.description = description
    return embed


def id_generator(
    size=6, 
    chars=string.ascii_uppercase + string.digits
) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

intervals = (
    ('y', 220752000), # year
    ('m', 18144000), # month
    ('w', 604800), # week
    ('d', 86400), # day
    ('h', 3600), # hour
    ('m', 60), # month
    ('s', 1), # second
)

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def is_url_image(image_url) -> bool:
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False

def display_channels(
    indent: str, 
    list_of_channelIDs
) -> str:
    result = ""
    for channel_id in list_of_channelIDs:
        result += f"{indent}<#{channel_id}>\n"
    return result

def display_users(
    indent: str, 
    list_of_userIDs
) -> str:
    result = ""
    for user_id in list_of_userIDs:
        result += f"{indent}<@{user_id}>\n"
    return result

def validateBotOwner(id):
    return True if (int(id) in config.idlist_admin) or int(id) == config.blueID else False
    
