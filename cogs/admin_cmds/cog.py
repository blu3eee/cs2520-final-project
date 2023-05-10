# standard 
import json
import time
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
from nextcord.ext import commands

from typing import Optional
import nextcord, pytz
from datetime import datetime

# Local
import config
from utils.list_json_utils import add_list_json, remove_list_json
from utils.utils import display_channels, display_users
from utils.json_utils import jsonfile_get_data, jsonfile_save_data

class AdminInteractions(Cog, name="<:blurplecertifiedmoderator:963564382686703686> Admistrator"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="bot")
    @is_owner()
    async def commands_bot(self, ctx: Context, bot_status):
        stats = ["on", "off"]
        if bot_status in stats:
            file_name = "general.json"
            general_data = jsonfile_get_data(file_name)
            if f"{ctx.guild.id}" not in general_data:
                general_data[f"{ctx.guild.id}"] = {}
            general_data[f"{ctx.guild.id}"]["bot_status"] = bot_status
            jsonfile_save_data(file_name=file_name, file_data=general_data)
            await ctx.message.add_reaction(config.check_emoji)
        else:
            await ctx.message.add_reaction(config.cross_emoji)

    @command(name="chat", aliases = ["speak", "repeat"])
    @has_permissions(administrator=True)
    async def _repeat(self, ctx: Context, *, content):
        """Use bot to repeat what you said"""
        await ctx.channel.purge(limit=1, check=lambda m: m.author == ctx.author)
        await ctx.send(content)

    @command(name="embed")
    async def _embed(self, ctx: Context, *, content):
        """Use bot create embed"""
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge(limit=1, check=lambda m: m.author == ctx.author)
            embed = Embed(
                description=content,
                color=config.theme_color
            )
            await ctx.send(embed=embed)

    @group(name="blacklist", aliases = ["bll"], invoke_without_command = True)
    @is_owner()
    async def _blacklist(self, ctx: Context):
        """Show Blacklist command(s) list"""
        await ctx.reply(
            embed = Embed(
                description=f"**Blacklist command(s) list**\n\n"
                +f"{str(config.blank_emoji)}・**{config.PREFIX}blacklist** add [user1, user2, ...]\n"
                +f"{str(config.blank_emoji)}・**{config.PREFIX}blacklist** remove [user1, user2, ...]\n"
                +f"{str(config.blank_emoji)}・**{config.PREFIX}blacklist** list",
                color=config.colorless_hex
            ).set_footer(text=config.footer_str, icon_url=ctx.guild.icon)
        )

    @_blacklist.command(name="add", aliases = ["a"])
    @is_owner()
    async def _blacklist_add(self, ctx: Context, users: Greedy[User]):
        for user in users:
            if user.id != config.blueID:
                await add_list_json("general.json", ["bot_blacklist_users"], user.id)
        
    @_blacklist.command(name="remove", aliases = ["delete"])
    @is_owner()
    async def _blacklist_remove(self, ctx: Context, users: Greedy[User]):
        for user in users:
            await remove_list_json("general.json", ["bot_blacklist_users"], user.id)
    
    @_blacklist.command(name="list", aliases = ["danhsach"])
    @is_owner()
    async def _blacklist_list(self, ctx: Context):
        # open json file to read file_data
        file_name = "general.json"
        data_name = "bot_blacklist_users"
        with open(file_name,'r') as file:
            file_data = json.load(file)
            file.close()
        if data_name not in file_data:
            file_data[data_name] = []
        user_list = file_data[data_name]
        desc = display_users(f"{config.blank_emoji}・", user_list)
        await ctx.send(
            embed = Embed(
                description=f"**{ctx.guild.name} - Bot Blacklisted User(s)**\n\n{desc}",
                color = config.colorless_hex
            )
        )

    @command()
    async def embedlink(self, ctx: commands.Context, image_link, *, content):
        """Use bot to create embed with a picture (provided link)"""
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge(limit=1, check=lambda m: m.author == ctx.author)
            embed = Embed(
                description=content,
                color=config.theme_color
            )
            embed.set_image(url=image_link)
            await ctx.send(embed=embed)
            
    @command(name="member", pass_context = True)
    @has_permissions(administrator=True)
    async def _member(self, ctx: commands.Context, member: Optional[Member]):
        # member created date
        user_created_timestamp = int(time.mktime(member.created_at.timetuple()))
        user_joined_at_timestamp = int(time.mktime(member.joined_at.timetuple()))
        
        embed = Embed(
            color=nextcord.Color.yellow()
        )
        member_type = "Bot" if member.bot is False else "User"
        embed.add_field(
            name=f"{member}",
            value=f"**{member_type} ID:** {member.id}\n"
            +f"**Joined Discord since**\n <t:{user_created_timestamp}>\n<t:{user_created_timestamp}:R>\n"
            +f"**Display name:** {member.display_name}\n"
            +f"**Joined server since ** <t:{user_joined_at_timestamp}>",
            inline=False
        )
        for role in member.roles:
            roles_str=f"{role.name}, "
        embed.add_field(
            name="Roles",
            value=roles_str,
            inline=True
        )

        if member.banner is not None:
            embed.set_image(url=member.banner)
            if member.avatar is not None:
                embed.set_thumbnail(url=member.avatar)
        else:
            if member.avatar is not None:
                embed.set_image(url=member.avatar)
        await ctx.send(embed=embed)

    @command()
    @has_permissions(administrator=True)
    async def role(self, ctx: commands.Context, members: Greedy[Member], *, rolename: str):
        """add/remove roles for member"""
        try:
            role = None
            for role_irt in ctx.guild.roles:
                if rolename.lower() == role_irt.name.lower() :
                    role = role_irt
                    break
            if role == None:
                for role_irt in ctx.guild.roles:
                    if rolename.lower() in role_irt.name.lower() :
                        role = role_irt
                        break
            if role == None and rolename.isdecimal():
                role = ctx.guild.get_role(int(rolename))
            if role != None:
                #assert isinstance(role, nextcord.Role)
                for member in members:
                    if role not in member.roles:
                        await member.add_roles(role)
                        # send confirmation message
                        await ctx.send(
                            embed=Embed(
                                description=f"{str(config.check_emoji)} Added role `{role.name}` for {member.name}",
                                color=nextcord.Color.green()
                            )
                        )
                    elif role in member.roles:
                        await member.remove_roles(role)
                        await ctx.send(
                            embed=Embed(
                                description=f"{str(config.check_emoji)} Remove role `{role.name}` from {member.name}",
                                color=nextcord.Color.red()
                            )
                        )
            else:
                await ctx.send(
                    embed=Embed(
                        description=f"Can't find role `{rolename}`.",
                        color=nextcord.Color.red()
                    )
                )
        except Exception as e:
            print(e)

    @command()
    @has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, amount):
        try:
            await ctx.channel.purge(limit=int(amount))
        except Exception as e:
            print(e)
    
    @command()
    @has_permissions(administrator=True)
    async def purge(self, ctx: commands.Context, amount, mention: Optional[Member]):
        if mention is None:
            mention = ctx.author
        try:
            await ctx.message.delete()
            await ctx.channel.purge(limit=int(amount), check=lambda m: m.author == mention)
        except Exception as e:
            print(e)

    @command(name="kick")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_commands(self, ctx: Context, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
        if not len(targets):
            await ctx.send(
                embed=Embed(
                    description=f"`{config.PREFIX}kick [member] [reason]`",
                    color=config.theme_color
                )
            )
        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position:
                    await target.kick(reason=reason)
                    embed= Embed(
                        title="Member kicked",
                        color=0xDD2222,
                        timestamp=datetime.now(tz=config.vntz)
                    )
                    embed.set_thumbnail(url=target.avatar)

                    fields = [
                        ("Member", f"{target.name} a.k.a. {target.display_name}\n`ID: {target.id}`", False),
                        ("Actioned by", f"{ctx.author.display_name}\n`ID: {ctx.author.id}`", False),
                        ("Reason", reason, False)
                    ]
                    for name, value, inline in fields:
                        embed.add_field(
                            name=name,
                            value=value,
                            inline=inline
                        )
                    # log_channel = self.bot.get_channel(config.CHANNEL_BOT_LOG)
                    # await log_channel.send(embed=embed)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(
                        embed = Embed(
                            description=f"I can't kick {target.display_name} a.k.a <@{target.id}>."
                        )
                    )
            
    @kick_commands.error
    async def kick_command_error(self, ctx: Context, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send(f"<@{ctx.message.author.id}>, you can't kick this member.")
    
    @command(name="ban")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_commands(self, ctx: Context, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
        if not len(targets):
            await ctx.send(
                embed=Embed(
                    description=f"`{config.PREFIX}ban [member] [reason]`",
                    color=config.theme_color
                )
            )
        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissions.administrator:
                    await target.ban(reason=reason)
                    embed= Embed(
                        title="Member banned",
                        color=0xDD2222,
                        timestamp=datetime.now(tz=config.vntz)
                    )
                    embed.set_thumbnail(url=target.avatar)

                    fields = [
                        ("Member", f"{target.name} a.k.a. {target.display_name}\n`ID: {target.id}`", False),
                        ("Actioned by", f"{ctx.author.display_name}\n`ID: {ctx.author.id}`", False),
                        ("Reason", reason, False)
                    ]
                    for name, value, inline in fields:
                        embed.add_field(
                            name=name,
                            value=value,
                            inline=inline
                        )
                    # log_channel = self.bot.get_channel(config.CHANNEL_BOT_LOG)
                    # await log_channel.send(embed=embed)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(
                        embed = Embed(
                            description=f"I can't ban {target.display_name} a.k.a. <@{target.id}>"
                        )
                    )
            
    @ban_commands.error
    async def ban_commands_error(self, ctx: Context, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send(f"<@{ctx.message.author.id}>, you can't ban this member.")

def setup(bot: commands.Bot):
    bot.add_cog(AdminInteractions(bot))

