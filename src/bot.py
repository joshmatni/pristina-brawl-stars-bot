import discord
from discord.ext import commands

# Load configuration
import config

# Initialize bot
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(config.DISCORD_TOKEN)

import requests

def get_player_stats(tag):
    url = f"https://api.brawlstars.com/v1/players/%23{tag}"
    headers = {
        'Authorization': f'Bearer {config.BRAWL_API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()
