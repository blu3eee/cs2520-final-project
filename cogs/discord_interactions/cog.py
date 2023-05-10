# standard
from pydoc import describe
import re
import nextcord, pytz, time
from datetime import datetime, date, timedelta
from typing import Optional

from operator import itemgetter

# nextcord
from nextcord import Embed, Member, User, Color
from nextcord.ext import commands
from nextcord.ext.commands import (
    Cog,
    Context,
    Greedy,
    Converter,
    CheckFailure,
    Bot,
    group,
    command,
    is_owner,
    has_permissions,
    guild_only,
    bot_has_permissions
)

# database
# from autoresponse_db import AutoResponseDatabase
# from general_db import GeneralData
# from general_db_list import GeneralDataList
# local
import config

# road ad regex, thanks road
invitere = r"(?:https?:\/\/)?discord(?:\.gg|app\.com\/invite)?\/(?:#\/)([a-zA-Z0-9-]*)"
# my own regex
invitere2 = r"(http[s]?:\/\/)*discord((app\.com\/invite)|(\.gg))\/(invite\/)?(#\/)?([A-Za-z0-9\-]+)(\/)?"

class DiscordInteractions(commands.Cog, name="<:blurplemembers:963564232123777065> General Information"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.snipes = {}

        @bot.listen('on_message_delete')
        async def on_message_delete(msg:nextcord.Message):
            try:
                list_msg=self.snipes[msg.channel.id]
                list_msg.append(msg)
                self.snipes[msg.channel.id] = list_msg
            except Exception as e:
                self.snipes[msg.channel.id] = [msg]
            if len(self.snipes[msg.channel.id]) > 10:
                list_msg = self.snipes[msg.channel.id]
                del list_msg[0]
                self.snipes[msg.channel.id] = list_msg

    @command(name="snipe", aliases = ["sn"])
    async def snipe(self, ctx: Context, howmany  = "1"):
        '"Snipes" someone\'s message that\'s been deleted.'
        try:
            snipe_list = self.snipes[ctx.channel.id]
        except KeyError:
            return await ctx.send('No deleted messages found!')
        if snipe_list is None:
            return await ctx.send('No deleted messages found!')
        # there's gonna be a snipe after this point
        emb = Embed(
            color=config.theme_color
        )
        howmany = int(howmany) if howmany.isdigit() else 1
        if int(howmany) <= 10:
            if len(snipe_list) >= int(howmany):
                snipe = snipe_list[len(snipe_list)-int(howmany)]
                emb.set_author(
                    name=str(snipe.author),
                    icon_url=snipe.author.display_avatar
                )
                emb.description = self.sanitise(snipe.content)
                emb.timestamp = snipe.created_at
                emb.set_footer(
                    text=f'Message sniped by {str(ctx.author)}'
                )
                if snipe.attachments:
                    bob = snipe.attachments[0]
                    bob_proxy_url = bob.proxy_url
                    emb.set_image(url=bob_proxy_url)
            else:
                emb.description = f"**Only {len(snipe_list)} delete messages in this channel are saved!**"
        else:
            emb.description  = "**The saving limit of deleted messages is capped at 10!**"
        await ctx.send(embed=emb)

    @command(name="serverinfo", aliases = ["svinfo"])
    async def _serverinfo(self, ctx: Context):
        """Check info server"""
        embed = Embed(
            title=f"Server Information - {ctx.guild.name}",
            description=ctx.guild.description if ctx.guild.description is not None else "",
            color=config.theme_color
        ).set_thumbnail(
            url=ctx.guild.icon
        ).set_author(
            name=ctx.guild.owner, 
            icon_url=ctx.guild.icon
        ).set_footer(
            text=self.bot.user.display_name, 
            icon_url=self.bot.user.display_avatar
        )
        if ctx.guild.banner is not None:
            embed.set_image(url=ctx.guild.banner)
        fields = [
            ("Owner", ctx.guild.owner, True),
            ("Server ID", ctx.guild.id, True),
            ("Member Count", ctx.guild.member_count, True),
            ("Created At", f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}>", True),
            ("Boost Tier", f"Level {ctx.guild.premium_tier}/3", True),
            ("Boost Count", ctx.guild.premium_subscription_count, True),
        ]
        for field_name, field_value, field_inline in fields:
            embed.add_field(
                name=field_name,
                value=field_value,
                inline=field_inline
            )
        await ctx.send(embed=embed)

    @command(name="boosters")
    @is_owner()
    async def _boosters(self, ctx: Context):
        list_dscrptn = ""
        for member in ctx.guild.premium_subscribers:
            list_dscrptn += f"\n{config.blank_emoji}・**{member}** - {member.mention} - {member.id}"
        await ctx.send(
            embed = Embed(
                description=f"**List - Server booster(s)**\n{list_dscrptn}"
            ).set_thumbnail(
                url=ctx.guild.icon
            ).set_author(
                name=ctx.guild.owner, 
                icon_url=ctx.guild.icon
            ).set_footer(
                text=config.footer_str, 
                icon_url=self.bot.user.display_avatar
            )
        )        

    @command(name="user", aliases = ["profile", "prof", "whois"])
    async def _user(self, ctx: Context, user: Optional[User]):
        """Get Discord user's info"""
        user = ctx.author if user is None else user       
        # member created date
        embed = Embed(
            color=nextcord.Color.yellow()
        )
        member_type  = "User" if user.bot is False else "Bot"
        member_created_timestamp = int(time.mktime(ctx.guild.created_at.timetuple()))
        embed.add_field(
            name=f"{user}",
            value=f"**{member_type} ID:** {user.id}\n"
            +f"**Joined Discord:** <t:{member_created_timestamp}>\n(<t:{member_created_timestamp}>)\n"
            +f"**Display name:** {user.display_name} a.k.a. <@{user.id}>\n",
            inline=False
        )

        mentioned_user2 = await self.bot.fetch_user(user.id)
        if mentioned_user2.banner is not None:
            embed.set_image(url=mentioned_user2.banner)
            if mentioned_user2.avatar is not None:
                embed.set_thumbnail(url=mentioned_user2.avatar)
        else:
            if mentioned_user2.avatar is not None:
                embed.set_image(url=mentioned_user2.avatar)

        await ctx.send(embed=embed)


    @command(aliases = ["ava", "av"])
    async def avatar(self, ctx: Context, user: Optional[User]):
        """Get Discord user's avatar"""
        user = ctx.author if user is None else user

        embed = Embed(
            color=config.theme_color
        )
        member_type  = "User" if user.bot is False else "Bot"
        embed = Embed(
            description=f"{user}\n**{member_type} ID:** {user.id}\n",
            color=config.theme_color
        )

        mentioned_user2 = await self.bot.fetch_user(user.id)
        if mentioned_user2.avatar is not None:
            embed.set_image(url=mentioned_user2.avatar)
            try:
                mentioned_member = await ctx.guild.fetch_member(mentioned_user2.id)
                if mentioned_member.guild_avatar is not None:
                    embed.set_image(url=mentioned_member.guild_avatar)                    
            except Exception as e:
                print(e)
        else:
            try:
                mentioned_member = await ctx.guild.fetch_member(mentioned_user2.id)
                if mentioned_member.guild_avatar is not None:
                    embed.set_image(url=mentioned_member.guild_avatar)                 
            except Exception as e:
                print(e)
                embed.set_image(url=mentioned_member.display_avatar)  

        await ctx.send(embed=embed)
  

    @command(pass_context = True)
    async def banner(self, ctx: Context, user: Optional[User]):
        """Get Discord user's banner"""
        user = ctx.author if user is None else user
        
        member_type  = "User" if user.bot is False else "Bot"
        embed = Embed(
            description=f"{user}\n**{member_type} ID:** {user.id}\n",
            color=config.theme_color
        )

        mentioned_user2 = await self.bot.fetch_user(user.id)
        if mentioned_user2.banner is not None:
            embed.set_image(url=mentioned_user2.banner)
        else:
            embed.add_field(
                name="This user doesn't have a banner.",
                value="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
            )    

def setup(bot: Bot):
    bot.add_cog(DiscordInteractions(bot))
