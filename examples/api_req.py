import requests

# Replace with your bot token
BOT_TOKEN = "your-bot-token-goes-here"

# Replace with the channel ID where you want to send the message
CHANNEL_ID = "your-channel-id-goes-here"

# Define the message content
message_content = "Hello, this is a test message from my bot!"

# Define the API endpoint
url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"

# Set the headers
headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

# Set the payload
payload = {
    "content": message_content
}

# Send the request
response = requests.post(url, json=payload, headers=headers)

# Check the response
if response.status_code == 200:
    print("Message sent successfully!")
else:
    print(f"Failed to send message, status code: {response.status_code}")
