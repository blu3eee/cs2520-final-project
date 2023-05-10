# standard
from typing import Optional

# nextcord
from nextcord.ext import commands
from nextcord.ext.commands import (
    Bot,
    command,
)

class Math(commands.Cog, name="Math"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @command(name="math", aliases = ["calc", "cal"])
    async def command_math(
        self, 
        ctx: commands.Context, 
        *, expression : Optional[str]
    ):
        try:
            if expression is not None:
                result = eval(expression)
                await ctx.message.reply(f"{result}")
        except Exception as e:
            await ctx.message.reply(
                "***Not a valid basic math expression!***"
            )

def setup(bot: Bot):
    bot.add_cog(Math(bot))
