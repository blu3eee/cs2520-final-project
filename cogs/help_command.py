import nextcord
from nextcord.ext import commands
import config
from nextcord import Embed, Member

COLOR = config.theme_color
async def get_cog_help(cog: commands.Cog, ctx: commands.Context) -> Embed:
    cog = ctx.bot.get_cog(cog)
    
    embed = Embed(color=COLOR)
    embed.title = cog.__cog_name__ + " Commands"
    embed.description = "\n".join(
        f"`{command.name}`: {command.help}"
        for command in cog.get_commands()
        #if not isinstance(command, nextcord.ApplicationCommand)
    )
    embed.description = f"Type `{ctx.clean_prefix}help <command>` to see more info of the command\n\n**Commands:**\n{embed.description}"
    return embed
        
class HelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        bot = self.context.bot
        embed = Embed(
            title=bot.user.name,
            description=f"For more info on a command: `{self.context.clean_prefix}help <command>`",
            colour=COLOR,
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="Server Count", value=len(bot.guilds))
        embed.add_field(name="User Count", value=len(bot.users))
        embed.add_field(name="Ping", value=f"{bot.latency*1000:.2f}ms")

        for cog, commands in mapping.items():
            if cog and commands and cog.__cog_name__ not in ["Jishaku", "Pycord", "Developer"]:
                cog = bot.get_cog(cog.__cog_name__)
                description = " ".join(
                    f"`{command.name}`"
                    for command in cog.get_commands()
                    #if not isinstance(command, nextcord.ApplicationCommand)
                )
                embed.add_field(name=cog.__cog_name__, value=description, inline=False)
        embed.set_footer(text=f"For more info on a command: `{self.context.clean_prefix}help <command>`")
        await self.context.send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        await self.context.send(embed=get_cog_help(cog.__cog_name__, self.context))

    async def send_group_help(self, group: commands.Group):
        params = []
        parents = group.parents
        for parent in parents:
            params.append(parent.qualified_name)
        print(params)
        params.reverse()
        params.extend([group.name])
        params.extend([group.signature])

        usage_description = " ".join(params)
        embed = Embed(title=group.name, description=group.help, color=COLOR)
        embed.add_field(
            name="Usage",
            value=f"{self.context.prefix}{usage_description}",
        )
        if len(group.commands):
            embed.add_field(
                name="Subcommands",
                value=", ".join(i.name for i in group.commands if not i.hidden),
                inline=False,
            )
        await self.context.send(embed=embed)

    async def send_command_help(self, command: commands.Command):
        aliases_str = ", ".join(command.aliases) if len(command.aliases) > 0 else "none"
        params = []
        parents = command.parents
        for parent in parents:
            params.append(parent.qualified_name)
        print(params)
        params = [params[0]] if len(params) > 0 else []
        params.reverse()
        params.extend([command.name])
        params.extend([command.signature])

        usage_description = " ".join(params)

        embed = Embed(
            title=command.name,
            description=f"**Usage:** `{self.context.prefix}{usage_description}`\n"
            +f"**Aliases:** `{aliases_str}`\n"
            +f"**Category:** {command.cog_name}\n"
            +f"**Description:** {command.help}\n",
            color=COLOR,
        )
        embed.set_footer(text="For more support, please contact blu3eee#1102")
        await self.context.send(embed=embed)


def setup(bot: commands.Bot):
    bot._default_help_command = bot.help_command
    bot.help_command = HelpCommand()


def teardown(bot: commands.Bot):
    bot.help_command = bot._default_help_command
