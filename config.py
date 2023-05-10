import os, pytz
import nextcord
from dotenv import load_dotenv
load_dotenv()
# Bot setup
PREFIX = "a"
PREFIX_LIST = ['a', 'A']
BOT_NAME = "asian kid"
BOT_TOKEN = os.getenv('BOT_TOKEN')

vntz = pytz.timezone("Asia/Ho_Chi_Minh")

#mybot
footer_str = "© Bot by @blu3eee#4287"
thumbnail_url = "https://media.discordapp.net/attachments/1012855216535781426/1022288570515476530/ae17877b0bc91e470e6fa318e7a5a9cf.png"
author_url = "https://media.discordapp.net/attachments/1012855216535781426/1030640101677600849/HD-wallpaper-anime-character-bleu-anime-black-bleu-cartoon-fantasy-idea-iphone-minimal-sad-samsung-thumbnail.jpg"
#admin
blueID = 985772485154832525
idlist_admin = [blueID]
# colors
theme_color = 0x9df8f7
colorless_hex = 0x2f3136
# emojis
check_emoji = nextcord.PartialEmoji(name="blurple_check", id="981711532096368670")
cross_emoji = nextcord.PartialEmoji(name="blurple_X", id="981711531932807259")