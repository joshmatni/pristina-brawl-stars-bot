import os
from discord import Intents, Client, Message
from dotenv import load_dotenv
import responses
import joblib

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BS_API_KEY = os.getenv('BS_API_KEY')
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

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
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")

@client.event # handles incoming messages
async def on_message(message: Message) -> None:
    if message.author == client.user:  # so bot doesn't infinitely respond to itself
        return

    content = message.content
    if content.startswith('!predict1v1 '):
        args = content.split(' ')[1:]  # Get arguments after command
        if len(args) != 3:
            await message.channel.send("Usage: !predict1v1 <brawler> <player1_tag> <player2_tag>")
            return

        brawler, player1_tag, player2_tag = args
        player1_stats = responses.get_player_metrics(player1_tag, brawler)
        player2_stats = responses.get_player_metrics(player2_tag, brawler)
        if player1_stats and player2_stats:
            prediction_embed = responses.predict_outcome(player1_stats, player2_stats, player1_stats['player_name'], player2_stats['player_name'])
            await message.channel.send(embed=prediction_embed)
        else:
            await message.channel.send("Error fetching player statistics. Please check the tags and brawler names.")



def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
