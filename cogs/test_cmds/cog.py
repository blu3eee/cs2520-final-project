# standard 
import time
import json
# nextcord
from nextcord import (
    Embed, 
    Member,
    User
)
from nextcord.ext.commands import (
    Bot,
    Cog, 
    Greedy, 
    Context, 
    group,
    command, 
    has_permissions, 
    bot_has_permissions, 
    is_owner, 
    CheckFailure
)
from nextcord.embeds import Embed
from nextcord.ext import commands, menus

from typing import Optional
import nextcord, pytz
from datetime import datetime

# Local
import config
from utils.json_utils import jsonfile_get_data, jsonfile_save_data

class Test(Cog, name="<:earlydev:922060057162678273> Test"):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    
    
def setup(bot: commands.Bot):
    bot.add_cog(Test(bot))

class MyPageSource2(menus.ListPageSource):
    def __init__(self, bot: Bot, ctx, totalcash, data):
        # this is where you can set how many items you want per page
        self.bot = bot
        self.ctx = ctx
        self.total_cash = totalcash
        super().__init__(data, per_page=10)

    async def format_page(self, menu, entries):
        embed = nextcord.Embed(color=config.colorless_hex)
        desc = ""
        count = 0
        now_string = datetime.now(tz=config.vntz).strftime("%d/%m/%Y %H:%M:%S")
        for entry in entries:
            # cur_user = self.bot.get_user(int(entry[0]))
            desc +=  f"#{menu.current_page*10+count+1}    {entry[1]} {entry[0]}\n       {entry[2]} - {entry[3]}\n"
            count+=1
        embed.description = f"```md\n> Total estimate: {self.total_cash:,} VND\n\n\n{desc}\n\n{now_string}```"
        embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed