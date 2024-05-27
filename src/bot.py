import os
from discord import Intents, Client, Message
from discord.ext import commands
from dotenv import load_dotenv
import responses
import joblib

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BS_API_KEY = os.getenv('BS_API_KEY')
intents = Intents.default()
intents.message_content = True
#client = Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message was empty... (Intents not enabled properly")
        return
    
    if is_private := user_message[0] == "?":
        user_message = user_message[1:]
    
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e) # replace with logging


# handle start up for bot
@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is now running!")
    await bot.tree.sync()

@bot.hybrid_command(description="Compares two players using a specified brawler to predict the winner of a 1v1 match.")
async def predict1v1(ctx, brawler: str, player1_tag: str, player2_tag: str):
    if ctx.author == bot.user:  # Prevent bot from responding to itself
        return

    player1_stats = responses.get_player_metrics(player1_tag, brawler)
    player2_stats = responses.get_player_metrics(player2_tag, brawler)

    if player1_stats and player2_stats:
        prediction_embed = responses.predict_outcome(player1_stats, player2_stats, player1_stats['player_name'], player2_stats['player_name'])
        await ctx.send(embed=prediction_embed)  # Use `ctx.send()` to cover both message and interaction contexts
    else:
        await ctx.send("Error fetching player statistics. Please check the tags and brawler names.")


def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
