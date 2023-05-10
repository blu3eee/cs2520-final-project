import nextcord
from nextcord.ext import commands

# Replace with your bot token
BOT_TOKEN = "your-bot-token-goes-here"

# Replace with the channel ID where you want to send the message
CHANNEL_ID = 123456789012345678  # Use an actual channel ID as an integer

# Define the message content
message_content = "Hello, this is a test message from my bot!"

# Create the bot instance
bot = commands.Bot(command_prefix="!")

# Define the on_ready event
@bot.event
async def on_ready():
    print(f"{bot.user} is connected to Discord!")
    
    # Get the channel by its ID
    channel = bot.get_channel(CHANNEL_ID)
    
    # Send the message to the channel
    if channel:
        await channel.send(message_content)
    else:
        print("Channel not found")

# Start the bot
bot.run(BOT_TOKEN)