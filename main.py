# standards
from typing import Optional
from asyncpg import StringDataRightTruncation, StringDataRightTruncationError
import time, os

# nextcord
import nextcord
from nextcord import (
    Embed, 
    Color, 
)
from nextcord.ext import commands, tasks
from nextcord.ext.commands import (
    Context,
    CommandOnCooldown,
    MissingPermissions    
)
# locals
import config
from utils.utils import is_url_image
from utils.json_utils import jsonfile_get_data, jsonfile_save_data

def main():
    # allows privledged intents for monitoring members joining, roles editing, and role assignments
    intents = nextcord.Intents.all()
    intents.guilds = True
    intents.members = True
    
    bot = commands.Bot(
        command_prefix = config.PREFIX_LIST,
        intents = intents
    )
    bot.__status_index = 0
    
    @bot.event
    async def on_ready():
        print(f"{bot.user.name} has connected to Discord.")

    @bot.event
    async def on_command_error(ctx: Context, error): 
        print(error)
        # if cooldown
        if isinstance(error, CommandOnCooldown):
            await ctx.send(embed=Embed(title=f"Please slow down!",description=f"Try again after {error.retry_after:.2f} seconds.", color=config.theme_color).set_footer(text="For more support, please contact blu3eee#0001", icon_url=ctx.guild.icon), delete_after=error.retry_after)
            return
        # if string too long
        if isinstance(error, StringDataRightTruncation) or isinstance(error, StringDataRightTruncationError):
            await ctx.reply(embed=Embed(title=f"ERROR",description=f"String too long.",color=Color.red()).set_footer(text="For more support, please contact blu3eee#0001", icon_url=ctx.guild.icon))
            await ctx.message.add_reaction(config.cross_emoji)
            return

        # Missing Permission(s)
        if isinstance(error, MissingPermissions):
            missingPermissionString = ""
            for perm in error.missing_permissions:
                missingPermissionString += f"    +{perm}\n"
            await ctx.reply(embed=Embed(title=f"ERROR",description=f"- Missing Permission(s)\n{missingPermissionString}\n\nYou don't have permission to use this command..",color=Color.red()).set_footer(text="For more support, please contact blu3eee#0001", icon_url=ctx.guild.icon))
            await ctx.message.add_reaction(config.cross_emoji)
            return
        # send report to error channel(s) if error
        embedERROR = Embed(
            title=f"ERROR",
            description=f"**Error:** {error}\n\n**Message\Command:** {ctx.message.content}", 
            color=nextcord.Color.red()
        ).set_footer(text=f"User: {ctx.author} - ID: {ctx.author.id}", icon_url=ctx.author.display_avatar).set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        if len(ctx.message.attachments) > 0 and is_url_image(ctx.message.attachments[0].url):
            embedERROR.set_image(url=ctx.message.attachments[0].url)
                
        argumentErrors = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError)
        if isinstance(error, argumentErrors):
            command = ctx.command
            aliases_str  = ", ".join(command.aliases) if len(command.aliases) > 0 else "none"
            params = []
            for parent in command.parents:
                params.append(parent.qualified_name)
            print(params)
            params = [params[0]] if len(params) > 0 else []
            params.reverse()
            params.extend([command.name])
            params.extend([command.signature])

            usage_description  = " ".join(params)
 
            await ctx.send(
                embed = Embed(
                    title=command.name,
                    description=f"**Usage:** `{ctx.prefix}{usage_description}`\n"
                    +f"**Aliases:** `{aliases_str}`\n"
                    +f"**Category:** {command.cog_name}\n"
                    +f"**Description:** {command.help}\n",
                    color=config.theme_color,
                ).set_footer(
                    text="For more support, please contact blu3eee#0001"
                )
            )

    @bot.event    
    async def on_message(message: nextcord.Message):
        general_data = jsonfile_get_data("general.json")
        if f"{message.guild.id}" not in general_data:
            general_data[f"{message.guild.id}"] = {}
        if "bot_status" not in general_data[f"{message.guild.id}"]:
            general_data[f"{message.guild.id}"]["bot_status"] = "off"
        jsonfile_save_data("general.json", general_data) 
        if f"{config.PREFIX}bot" in message.content.lower():
            await bot.process_commands(message)  
        if general_data[f"{message.guild.id}"]["bot_status"] == "on":
            # PROCESSING COMMANDS IF VALID
            ctx: Context = await bot.get_context(message)
            if ctx.valid:
                general_data = jsonfile_get_data("general.json")
                # get blacklisted user(s)
                if "bot_blacklist_users" not in general_data:
                    general_data["bot_blacklist_users"] = []
                blacklisted_users = general_data["bot_blacklist_users"]
                # get locked channel(s)
                if "bot_blacklist_channels" not in general_data:
                    general_data["bot_blacklist_channels"] = []
                locked_channels = general_data["bot_blacklist_channels"]
                # get server's disabled command
                if f"{message.guild.id}" not in general_data:
                    general_data[f"{message.guild.id}"] = {}
                if "disabled_commands" not in general_data[f"{message.guild.id}"]:
                    general_data[f"{message.guild.id}"]["disabled_commands"] = []
                server_disabled_commands = general_data[f"{message.guild.id}"]["disabled_commands"]
                jsonfile_save_data("general.json", general_data) 
                # validation and process message
                if (
                    (ctx.author.guild_permissions.administrator) or 
                    (
                        ctx.author.id not in blacklisted_users and
                        ctx.channel.id not in locked_channels and
                        ctx.command.qualified_name not in server_disabled_commands
                    )
                ):  
                    # run command
                    await bot.process_commands(message)
            else:
                pass       

    @bot.command()
    async def ping(ctx: commands.Context):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send(f'Pong 🏓')
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")
        print(f'Ping {int(ping)}ms')

    @bot.command()
    async def load(ctx: commands.Context, extension: Optional[str]):
        """.load <extension> load extension to cogs"""
        if extension == None:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.load_extension(f'cogs.{filename[:-3]}')
            # load all cogs
            for folder in os.listdir("./cogs"):
                if os.path.exists(os.path.join("cogs", folder, "cog.py")):
                    bot.load_extension(f"cogs.{folder}.cog")
            await ctx.reply(
                embed=Embed(
                    description="Loaded all extensions.",
                    color=config.colorless_hex
                )
            )

    @bot.command()
    async def unload(ctx: commands.Context, extension: Optional[str]):
        """.unload <extension> unload extension from cogs"""
        if extension == None:
            # unload all cogs
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.unload_extension(f'cogs.{filename[:-3]}')
            for folder in os.listdir("./cogs"):
                if os.path.exists(os.path.join("cogs", folder, "cog.py")):
                    bot.unload_extension(f"cogs.{folder}.cog")
            await ctx.reply(
                embed=Embed(
                    description="Unloaded all extensions.",
                    color=config.colorless_hex
                )
            )
    
    @bot.command()
    async def reload (ctx: commands.Context, extension: Optional[str]):
        """.unload <extension> unload extension from cogs"""
        if extension == None:
            # unload all cogs
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.unload_extension(f'cogs.{filename[:-3]}')
            for folder in os.listdir("./cogs"):
                if os.path.exists(os.path.join("cogs", folder, "cog.py")):
                    bot.unload_extension(f"cogs.{folder}.cog")
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.load_extension(f'cogs.{filename[:-3]}')
            # load all cogs
            for folder in os.listdir("./cogs"):
                if os.path.exists(os.path.join("cogs", folder, "cog.py")):
                    bot.load_extension(f"cogs.{folder}.cog")
            await ctx.reply(
                embed=Embed(
                    description="Reloaded all extensions.",
                    color=config.colorless_hex
                )
         )

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
        
    # load all cogs
    for folder in os.listdir("./cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")

    @tasks.loop(seconds=5)
    async def change_status():
        """change bot status every 5 secs""" 
        
        status_dict = [
            # nextcord.Activity(type=nextcord.ActivityType.watching, name=""),
            nextcord.Activity(type=nextcord.ActivityType.listening, name=f"Spotify"),
        ]
        await bot.change_presence(activity=status_dict[bot.__status_index])
        status_index=(bot.__status_index+1)%len(status_dict)
        bot.__status_index = status_index

        
    @change_status.before_loop
    async def before():
        await bot.wait_until_ready()

    change_status.start()

    # run the bot
    bot.run(config.BOT_TOKEN)

if __name__ == "__main__":
    
    main()
