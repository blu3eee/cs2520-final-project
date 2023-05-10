from nextcord.ext.commands import (
    Bot,
    Cog, 
    Context
)
from nextcord.ext import commands
import nextcord

# Local
from utils.json_utils import jsonfile_get_data, jsonfile_save_data

class Welcome(Cog, name="<:blurpleannouncements:963564255129509961> Welcome"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.general_file = "general.json"  # Set the file path to your general.json file

        @bot.event
        async def on_member_join(member: nextcord.Member):
            # Get the guild ID and welcome channel ID
            guild_id = member.guild.id
            general_data = self.get_general_data()
            welcome_channel_id = general_data.get(str(guild_id), {}).get("welcome_channel_id", None)

            # If no welcome channel ID is set for this guild, do nothing
            if welcome_channel_id is None:
                return
            
            # Get the channel by its ID
            channel = bot.get_channel(welcome_channel_id)

            # Send the welcome message
            if channel:
                await channel.send(f"Hi, {member.mention}!")

                # Create an embed
                embed = nextcord.Embed(
                    title="Welcome to the server!",
                    description=f"{member.name} just joined.",
                    color=nextcord.Color.blue(),
                    timestamp=member.joined_at
                )

                # Set the author and icon
                embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar.url)

                # Set the footer with the member ID
                embed.set_footer(text=f"ID: {member.id}")

                # Send the embed
                await channel.send(embed=embed)
            else:
                print("Channel not found")

    def get_general_data(self):
        return jsonfile_get_data(self.general_file)

    def update_welcome_channel(self, guild_id: int, welcome_channel_id: int):
        general_data = self.get_general_data()
        if str(guild_id) not in general_data:
            general_data[str(guild_id)] = {}
        general_data[str(guild_id)]["welcome_channel_id"] = welcome_channel_id
        jsonfile_save_data(self.general_file, general_data)

    @commands.command(name="setwelcomechannel", aliases = ['setwlc'])
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_channel(self, ctx: Context, channel: nextcord.TextChannel):
        print(channel)
        guild_id = ctx.guild.id
        self.update_welcome_channel(guild_id, channel.id)
        await ctx.send(f"Welcome channel has been updated to {channel.mention}")
    
def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))
