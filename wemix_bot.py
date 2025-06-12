import discord
from discord.ext import tasks
import requests
import os
from keep_alive import keep_alive  # Keeps the bot running on Render

# Load bot token from environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    update_status.start()

@tasks.loop(minutes=10)
async def update_status():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=wemix-token&vs_currencies=usd'
        response = requests.get(url)
        data = response.json()
        price = data["wemix-token"]["usd"]

        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"WEMIX: ${price:.2f}"
        )
        await client.change_presence(activity=activity)

        print(f"Updated status: Watching WEMIX: ${price:.2f}")

    except Exception as e:
        print(f"Error fetching WEMIX price: {e}")

# Keep the bot alive on Render
keep_alive()

# Run the bot
client.run(TOKEN)
